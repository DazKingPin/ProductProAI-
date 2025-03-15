import cv2
import numpy as np
from PIL import Image
import logging
from skimage.feature import hog, local_binary_pattern
from skimage import color, exposure
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextureAnalyzer:
    """
    Class for analyzing textures in images.
    """
    
    def __init__(self):
        """
        Initialize the TextureAnalyzer.
        """
        logger.info("TextureAnalyzer initialized")
    
    def analyze_texture(self, image_path):
        """
        Analyze the texture of an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Texture analysis results including texture type, roughness, and pattern information
        """
        try:
            # Load image
            logger.info(f"Loading image from {image_path}")
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert to grayscale for texture analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Resize for faster processing
            resized = cv2.resize(gray, (256, 256))
            
            # Calculate Local Binary Pattern
            radius = 3
            n_points = 8 * radius
            lbp = local_binary_pattern(resized, n_points, radius, method='uniform')
            
            # Calculate LBP histogram
            n_bins = int(lbp.max() + 1)
            lbp_hist, _ = np.histogram(lbp, density=True, bins=n_bins, range=(0, n_bins))
            
            # Calculate HOG features
            hog_features, hog_image = hog(
                resized, 
                orientations=8, 
                pixels_per_cell=(16, 16),
                cells_per_block=(1, 1), 
                visualize=True, 
                block_norm='L2-Hys'
            )
            
            # Enhance HOG image for visualization
            hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
            
            # Calculate texture roughness using gradient magnitude
            sobelx = cv2.Sobel(resized, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(resized, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
            roughness = np.mean(gradient_magnitude)
            
            # Calculate texture uniformity using standard deviation
            uniformity = 1.0 / (1.0 + np.std(resized))
            
            # Calculate texture contrast
            contrast = np.std(resized) / 255.0
            
            # Calculate texture directionality using HOG
            directionality = np.std(hog_features)
            
            # Determine texture type based on features
            texture_type = self._determine_texture_type(roughness, uniformity, contrast, directionality)
            
            # Determine pattern type
            pattern_type = self._determine_pattern_type(lbp_hist, hog_features)
            
            # Create texture analysis results
            texture_analysis = {
                'texture_type': texture_type,
                'roughness': float(roughness),
                'uniformity': float(uniformity),
                'contrast': float(contrast),
                'directionality': float(directionality),
                'pattern_type': pattern_type,
                'features': {
                    'lbp_histogram': lbp_hist.tolist(),
                    'hog_features': hog_features.tolist()[:10]  # First 10 HOG features
                }
            }
            
            logger.info(f"Successfully analyzed texture: {texture_type}, roughness: {roughness:.2f}")
            return texture_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing texture: {str(e)}")
            return {
                'texture_type': 'unknown',
                'roughness': 0.0,
                'uniformity': 0.0,
                'contrast': 0.0,
                'directionality': 0.0,
                'pattern_type': 'unknown',
                'features': {}
            }
    
    def _determine_texture_type(self, roughness, uniformity, contrast, directionality):
        """
        Determine the texture type based on calculated features.
        
        Args:
            roughness (float): Texture roughness value
            uniformity (float): Texture uniformity value
            contrast (float): Texture contrast value
            directionality (float): Texture directionality value
            
        Returns:
            str: Texture type
        """
        # These thresholds are approximate and may need adjustment
        if roughness < 10:
            if uniformity > 0.5:
                return "Smooth"
            else:
                return "Matte"
        elif roughness < 30:
            if directionality > 0.5:
                return "Striated"
            else:
                return "Textured"
        else:
            if contrast > 0.3:
                return "Rough"
            else:
                return "Coarse"
    
    def _determine_pattern_type(self, lbp_hist, hog_features):
        """
        Determine the pattern type based on LBP histogram and HOG features.
        
        Args:
            lbp_hist (ndarray): LBP histogram
            hog_features (ndarray): HOG features
            
        Returns:
            str: Pattern type
        """
        # Calculate entropy of LBP histogram as a measure of pattern complexity
        lbp_entropy = -np.sum(lbp_hist * np.log2(lbp_hist + 1e-10))
        
        # Calculate mean and std of HOG features
        hog_mean = np.mean(hog_features)
        hog_std = np.std(hog_features)
        
        # Determine pattern type based on features
        if lbp_entropy < 3.0:
            return "Solid"
        elif lbp_entropy < 4.0:
            if hog_std < 0.1:
                return "Uniform"
            else:
                return "Gradient"
        elif lbp_entropy < 5.0:
            if hog_mean > 0.2:
                return "Geometric"
            else:
                return "Organic"
        else:
            if hog_std > 0.2:
                return "Complex"
            else:
                return "Random"
    
    def save_texture_visualization(self, image_path, output_dir):
        """
        Create and save visualizations of texture analysis.
        
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
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Resize for faster processing
            resized = cv2.resize(gray, (256, 256))
            
            # Calculate Local Binary Pattern
            radius = 3
            n_points = 8 * radius
            lbp = local_binary_pattern(resized, n_points, radius, method='uniform')
            
            # Calculate HOG features
            _, hog_image = hog(
                resized, 
                orientations=8, 
                pixels_per_cell=(16, 16),
                cells_per_block=(1, 1), 
                visualize=True, 
                block_norm='L2-Hys'
            )
            
            # Enhance HOG image for visualization
            hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
            
            # Calculate gradient magnitude
            sobelx = cv2.Sobel(resized, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(resized, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
            gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Create visualization
            lbp_normalized = cv2.normalize(lbp, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            hog_normalized = (hog_image_rescaled * 255).astype(np.uint8)
            
            # Create a 2x2 grid of images
            h, w = resized.shape
            visualization = np.zeros((h*2, w*2), dtype=np.uint8)
            visualization[0:h, 0:w] = resized
            visualization[0:h, w:2*w] = lbp_normalized
            visualization[h:2*h, 0:w] = gradient_magnitude
            visualization[h:2*h, w:2*w] = hog_normalized
            
            # Add labels
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(visualization, 'Original', (10, 20), font, 0.5, 255, 1, cv2.LINE_AA)
            cv2.putText(visualization, 'LBP', (w+10, 20), font, 0.5, 255, 1, cv2.LINE_AA)
            cv2.putText(visualization, 'Gradient', (10, h+20), font, 0.5, 255, 1, cv2.LINE_AA)
            cv2.putText(visualization, 'HOG', (w+10, h+20), font, 0.5, 255, 1, cv2.LINE_AA)
            
            # Generate output filename
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            output_path = os.path.join(output_dir, f"{file_name}_texture.png")
            
            # Save visualization
            cv2.imwrite(output_path, visualization)
            logger.info(f"Texture visualization saved to {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating texture visualization: {str(e)}")
            return None


if __name__ == "__main__":
    # Example usage
    analyzer = TextureAnalyzer()
    
    # Test with a sample image if available
    test_image = "sample.jpg"  # Replace with an actual image path for testing
    if os.path.exists(test_image):
        texture_analysis = analyzer.analyze_texture(test_image)
        print("Texture analysis:", texture_analysis)
        
        # Save visualization
        analyzer.save_texture_visualization(test_image, "./output")
