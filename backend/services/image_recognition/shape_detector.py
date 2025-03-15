import cv2
import numpy as np
from PIL import Image
import logging
import os
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks
from skimage.measure import find_contours, approximate_polygon
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShapeDetector:
    """
    Class for detecting and analyzing shapes in images.
    """
    
    def __init__(self):
        """
        Initialize the ShapeDetector.
        """
        logger.info("ShapeDetector initialized")
    
    def detect_shapes(self, image_path):
        """
        Detect and analyze shapes in an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Shape analysis results including dominant shapes, edges, and contours
        """
        try:
            # Load image
            logger.info(f"Loading image from {image_path}")
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Resize for faster processing
            resized = cv2.resize(gray, (512, 512))
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(resized, (5, 5), 0)
            
            # Detect edges using Canny edge detector
            edges = canny(blurred, sigma=2.0)
            
            # Find contours
            contours = find_contours(edges, 0.8)
            
            # Analyze contours
            shape_info = self._analyze_contours(contours, resized.shape)
            
            # Detect lines using Hough transform
            line_info = self._detect_lines(edges)
            
            # Detect circles using Hough transform
            circle_info = self._detect_circles(blurred)
            
            # Determine dominant shapes
            dominant_shapes = self._determine_dominant_shapes(shape_info, line_info, circle_info)
            
            # Create shape analysis results
            shape_analysis = {
                'dominant_shapes': dominant_shapes,
                'shape_count': len(shape_info['shapes']),
                'has_straight_lines': line_info['has_straight_lines'],
                'has_curves': circle_info['has_circles'],
                'shape_complexity': shape_info['complexity'],
                'shape_distribution': shape_info['distribution'],
                'shape_details': shape_info['shapes'][:5]  # Limit to first 5 shapes for brevity
            }
            
            logger.info(f"Successfully detected shapes: {dominant_shapes}")
            return shape_analysis
            
        except Exception as e:
            logger.error(f"Error detecting shapes: {str(e)}")
            return {
                'dominant_shapes': ['Unknown'],
                'shape_count': 0,
                'has_straight_lines': False,
                'has_curves': False,
                'shape_complexity': 'Low',
                'shape_distribution': 'Unknown',
                'shape_details': []
            }
    
    def _analyze_contours(self, contours, image_shape):
        """
        Analyze contours to identify shapes.
        
        Args:
            contours (list): List of contours
            image_shape (tuple): Shape of the image
            
        Returns:
            dict: Information about shapes
        """
        shapes = []
        total_area = image_shape[0] * image_shape[1]
        covered_area = 0
        
        for contour in contours:
            # Skip very small contours
            if len(contour) < 5:
                continue
            
            # Approximate the contour
            approx = approximate_polygon(contour, tolerance=0.02)
            
            # Calculate contour properties
            area = cv2.contourArea(approx.astype(np.float32))
            perimeter = cv2.arcLength(approx.astype(np.float32), True)
            
            # Skip very small shapes
            if area < 100:
                continue
            
            # Calculate shape metrics
            compactness = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
            
            # Determine shape type
            shape_type = self._identify_shape(approx, compactness)
            
            # Calculate bounding box
            x_min, y_min = np.min(approx, axis=0)
            x_max, y_max = np.max(approx, axis=0)
            width = x_max - x_min
            height = y_max - y_min
            
            # Calculate aspect ratio
            aspect_ratio = width / height if height > 0 else 0
            
            # Add shape information
            shapes.append({
                'type': shape_type,
                'vertices': len(approx),
                'area': float(area),
                'perimeter': float(perimeter),
                'compactness': float(compactness),
                'aspect_ratio': float(aspect_ratio),
                'position': {
                    'x': float(np.mean(approx[:, 0])),
                    'y': float(np.mean(approx[:, 1]))
                }
            })
            
            covered_area += area
        
        # Calculate shape complexity
        if len(shapes) < 3:
            complexity = 'Low'
        elif len(shapes) < 10:
            complexity = 'Medium'
        else:
            complexity = 'High'
        
        # Calculate shape distribution
        coverage_ratio = covered_area / total_area
        if coverage_ratio < 0.2:
            distribution = 'Sparse'
        elif coverage_ratio < 0.5:
            distribution = 'Moderate'
        else:
            distribution = 'Dense'
        
        return {
            'shapes': shapes,
            'complexity': complexity,
            'distribution': distribution
        }
    
    def _identify_shape(self, contour, compactness):
        """
        Identify the type of shape based on contour properties.
        
        Args:
            contour (ndarray): Contour points
            compactness (float): Shape compactness
            
        Returns:
            str: Shape type
        """
        vertices = len(contour)
        
        # Circle detection
        if compactness > 0.8:
            return "Circle"
        
        # Polygon detection
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            # Check if it's a square or rectangle
            x_min, y_min = np.min(contour, axis=0)
            x_max, y_max = np.max(contour, axis=0)
            width = x_max - x_min
            height = y_max - y_min
            aspect_ratio = width / height if height > 0 else 0
            
            if 0.9 < aspect_ratio < 1.1:
                return "Square"
            else:
                return "Rectangle"
        elif vertices == 5:
            return "Pentagon"
        elif vertices == 6:
            return "Hexagon"
        elif vertices > 6 and vertices < 15:
            return "Polygon"
        else:
            return "Organic"
    
    def _detect_lines(self, edges):
        """
        Detect straight lines in an image using Hough transform.
        
        Args:
            edges (ndarray): Edge image
            
        Returns:
            dict: Information about detected lines
        """
        # Perform Hough transform
        tested_angles = np.linspace(-np.pi/2, np.pi/2, 180, endpoint=False)
        h, theta, d = hough_line(edges, theta=tested_angles)
        
        # Find peaks in Hough transform
        peaks = hough_line_peaks(h, theta, d, num_peaks=10)
        
        # Extract line information
        lines = []
        for _, angle, dist in zip(*peaks):
            # Calculate line orientation (horizontal, vertical, diagonal)
            if np.abs(angle) < 0.1 or np.abs(angle - np.pi/2) < 0.1:
                orientation = "Vertical"
            elif np.abs(angle - np.pi/4) < 0.1 or np.abs(angle + np.pi/4) < 0.1:
                orientation = "Diagonal"
            else:
                orientation = "Horizontal"
            
            lines.append({
                'angle': float(angle),
                'distance': float(dist),
                'orientation': orientation
            })
        
        return {
            'lines': lines,
            'has_straight_lines': len(lines) > 0,
            'line_count': len(lines),
            'dominant_orientation': self._get_dominant_orientation(lines)
        }
    
    def _get_dominant_orientation(self, lines):
        """
        Determine the dominant orientation of lines.
        
        Args:
            lines (list): List of line information
            
        Returns:
            str: Dominant orientation
        """
        if not lines:
            return "None"
        
        orientations = [line['orientation'] for line in lines]
        orientation_counts = {
            'Horizontal': orientations.count('Horizontal'),
            'Vertical': orientations.count('Vertical'),
            'Diagonal': orientations.count('Diagonal')
        }
        
        return max(orientation_counts, key=orientation_counts.get)
    
    def _detect_circles(self, image):
        """
        Detect circles in an image using Hough transform.
        
        Args:
            image (ndarray): Grayscale image
            
        Returns:
            dict: Information about detected circles
        """
        # Detect circles using Hough transform
        circles = cv2.HoughCircles(
            image.astype(np.uint8),
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=10,
            maxRadius=100
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype(int)
            circle_info = []
            
            for x, y, r in circles:
                circle_info.append({
                    'center': (int(x), int(y)),
                    'radius': int(r)
                })
            
            return {
                'circles': circle_info,
                'has_circles': True,
                'circle_count': len(circle_info)
            }
        else:
            return {
                'circles': [],
                'has_circles': False,
                'circle_count': 0
            }
    
    def _determine_dominant_shapes(self, shape_info, line_info, circle_info):
        """
        Determine the dominant shapes in the image.
        
        Args:
            shape_info (dict): Shape information
            line_info (dict): Line information
            circle_info (dict): Circle information
            
        Returns:
            list: Dominant shapes
        """
        dominant_shapes = []
        
        # Count shape types
        shape_types = [shape['type'] for shape in shape_info['shapes']]
        shape_counts = {}
        
        for shape_type in shape_types:
            if shape_type in shape_counts:
                shape_counts[shape_type] += 1
            else:
                shape_counts[shape_type] = 1
        
        # Add dominant shapes based on counts
        if shape_counts:
            # Sort shapes by count
            sorted_shapes = sorted(shape_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Add top shapes
            for shape_type, count in sorted_shapes[:3]:
                if count > 1:
                    dominant_shapes.append(shape_type)
        
        # Add general shape categories
        if line_info['has_straight_lines'] and not dominant_shapes:
            dominant_shapes.append("Geometric")
        
        if circle_info['has_circles'] and "Circle" not in dominant_shapes:
            dominant_shapes.append("Circular")
        
        if not dominant_shapes:
            if shape_info['complexity'] == 'High':
                dominant_shapes.append("Complex")
            else:
                dominant_shapes.append("Organic")
        
        return dominant_shapes
    
    def save_shape_visualization(self, image_path, output_dir):
        """
        Create and save visualizations of shape detection.
        
        Args:
            image_path (str): Path to the image file
            output_dir (str): Directory to save the visualization
            
        Returns:
            str: Path to the saved visualization file
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert to RGB for matplotlib
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize for faster processing
            resized = cv2.resize(img_rgb, (512, 512))
            
            # Convert to grayscale
            gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Detect edges using Canny edge detector
            edges = canny(blurred, sigma=2.0)
            
            # Find contours
            contours = find_contours(edges, 0.8)
            
            # Create visualization
            plt.figure(figsize=(12, 8))
            
            # Original image
            plt.subplot(2, 2, 1)
            plt.imshow(resized)
            plt.title('Original Image')
            plt.axis('off')
            
            # Edge detection
            plt.subplot(2, 2, 2)
            plt.imshow(edges, cmap='gray')
            plt.title('Edge Detection')
            plt.axis('off')
            
            # Contour visualization
            plt.subplot(2, 2, 3)
            plt.imshow(resized)
            for contour in contours:
                plt.plot(contour[:, 1], contour[:, 0], 'r-', linewidth=1)
            plt.title('Contours')
            plt.axis('off')
            
            # Shape approximation
            plt.subplot(2, 2, 4)
            plt.imshow(np.zeros_like(resized))
            for contour in contours:
                if len(contour) > 5:
                    approx = approximate_polygon(contour, tolerance=0.02)
                    plt.plot(approx[:, 1], approx[:, 0], 'g-', linewidth=2)
            plt.title('Shape Approximation')
            plt.axis('off')
            
            # Generate output filename
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            output_path = os.path.join(output_dir, f"{file_name}_shapes.png")
            
            # Save visualization
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()
            
            logger.info(f"Shape visualization saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating shape visualization: {str(e)}")
            return None


if __name__ == "__main__":
    # Example usage
    detector = ShapeDetector()
    
    # Test with a sample image if available
    test_image = "sample.jpg"  # Replace with an actual image path for testing
    if os.path.exists(test_image):
        shape_analysis = detector.detect_shapes(test_image)
        print("Shape analysis:", shape_analysis)
        
        # Save visualization
        detector.save_shape_visualization(test_image, "./output")
