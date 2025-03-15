import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ColorExtractor:
    """
    Class for extracting dominant colors from images.
    """
    
    def __init__(self, n_colors=5):
        """
        Initialize the ColorExtractor.
        
        Args:
            n_colors (int): Number of dominant colors to extract
        """
        self.n_colors = n_colors
        logger.info(f"ColorExtractor initialized with {n_colors} colors")
    
    def extract_colors(self, image_path):
        """
        Extract dominant colors from an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            list: List of dominant colors in hex format
            dict: Additional color information including RGB values and percentages
        """
        try:
            # Load image
            logger.info(f"Loading image from {image_path}")
            img = Image.open(image_path)
            img = img.resize((150, 150))  # Resize for faster processing
            img_array = np.array(img)
            
            # Reshape the image data for KMeans
            pixels = img_array.reshape(-1, 3)
            
            # Remove transparent pixels if image has alpha channel
            if img_array.shape[2] == 4:
                # Get alpha channel
                alpha = img_array[:, :, 3]
                # Create mask of non-transparent pixels
                mask = alpha > 0
                # Apply mask to get only non-transparent pixels
                pixels = img_array[mask][:, :3]
            
            # Apply KMeans clustering
            logger.info(f"Applying KMeans clustering to extract {self.n_colors} colors")
            kmeans = KMeans(n_clusters=self.n_colors, n_init=10)
            kmeans.fit(pixels)
            
            # Get the colors
            colors = kmeans.cluster_centers_.astype(int)
            
            # Calculate color percentages
            labels = kmeans.labels_
            color_counts = np.bincount(labels)
            color_percentages = color_counts / len(labels) * 100
            
            # Convert colors to hex format
            hex_colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in colors]
            
            # Create detailed color information
            color_info = {
                'hex': hex_colors,
                'rgb': colors.tolist(),
                'percentages': color_percentages.tolist()
            }
            
            # Sort colors by percentage
            sorted_indices = np.argsort(color_percentages)[::-1]
            sorted_hex_colors = [hex_colors[i] for i in sorted_indices]
            
            logger.info(f"Successfully extracted {len(sorted_hex_colors)} colors")
            return sorted_hex_colors, color_info
            
        except Exception as e:
            logger.error(f"Error extracting colors: {str(e)}")
            return [], {}
    
    def visualize_colors(self, colors, percentages=None, save_path=None):
        """
        Visualize the extracted colors.
        
        Args:
            colors (list): List of colors in hex format
            percentages (list, optional): List of color percentages
            save_path (str, optional): Path to save the visualization
            
        Returns:
            bool: True if visualization was successful, False otherwise
        """
        try:
            plt.figure(figsize=(10, 2))
            
            for i, color in enumerate(colors):
                percentage = percentages[i] if percentages else None
                plt.subplot(1, len(colors), i+1)
                plt.axpatch = plt.fill([0, 1, 1, 0], [0, 0, 1, 1], color=color)
                if percentage:
                    plt.title(f"{percentage:.1f}%", fontsize=10)
                plt.axis('off')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path)
                logger.info(f"Color visualization saved to {save_path}")
            
            plt.close()
            return True
            
        except Exception as e:
            logger.error(f"Error visualizing colors: {str(e)}")
            return False
    
    def get_color_palette(self, image_path, save_visualization=False, output_dir=None):
        """
        Extract and optionally visualize a color palette from an image.
        
        Args:
            image_path (str): Path to the image file
            save_visualization (bool): Whether to save the color visualization
            output_dir (str, optional): Directory to save the visualization
            
        Returns:
            dict: Color palette information including hex colors, RGB values, and percentages
        """
        # Extract colors
        hex_colors, color_info = self.extract_colors(image_path)
        
        if save_visualization and hex_colors and output_dir:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            output_path = os.path.join(output_dir, f"{file_name}_palette.png")
            
            # Visualize and save
            self.visualize_colors(hex_colors, color_info['percentages'], output_path)
        
        return {
            'hex_colors': hex_colors,
            'rgb_values': color_info.get('rgb', []),
            'percentages': color_info.get('percentages', [])
        }


if __name__ == "__main__":
    # Example usage
    extractor = ColorExtractor(n_colors=5)
    
    # Test with a sample image if available
    test_image = "sample.jpg"  # Replace with an actual image path for testing
    if os.path.exists(test_image):
        palette = extractor.get_color_palette(test_image, save_visualization=True, output_dir="./output")
        print("Extracted colors:", palette['hex_colors'])
