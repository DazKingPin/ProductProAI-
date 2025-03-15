import os
import logging
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelGenerator:
    """
    Class for generating 3D models or sketches from reference images.
    """
    
    def __init__(self):
        """
        Initialize the ModelGenerator.
        """
        logger.info("ModelGenerator initialized")
        self._load_feature_extractor()
    
    def _load_feature_extractor(self):
        """
        Load the pre-trained model for feature extraction.
        """
        try:
            logger.info("Loading pre-trained feature extraction model")
            # Use MobileNetV2 as a feature extractor (lightweight and fast)
            self.model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
            logger.info("Feature extraction model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading feature extraction model: {str(e)}")
            self.model = None
    
    def extract_features(self, image_path):
        """
        Extract features from an image using a pre-trained model.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            ndarray: Extracted features
        """
        try:
            if self.model is None:
                raise ValueError("Feature extraction model not loaded")
            
            # Load and preprocess the image
            img = keras_image.load_img(image_path, target_size=(224, 224))
            x = keras_image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            
            # Extract features
            features = self.model.predict(x)
            
            # Flatten features for easier processing
            flattened_features = features.flatten()
            
            logger.info(f"Successfully extracted {len(flattened_features)} features from image")
            return flattened_features
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return np.array([])
    
    def generate_model_parameters(self, image_path, shape_analysis, color_analysis, texture_analysis):
        """
        Generate 3D model parameters based on image analysis.
        
        Args:
            image_path (str): Path to the image file
            shape_analysis (dict): Shape analysis results
            color_analysis (dict): Color analysis results
            texture_analysis (dict): Texture analysis results
            
        Returns:
            dict: 3D model parameters
        """
        try:
            logger.info(f"Generating model parameters for {image_path}")
            
            # Extract features from the image
            features = self.extract_features(image_path)
            
            # Generate basic model parameters
            model_params = {
                'type': self._determine_model_type(shape_analysis),
                'dimensions': self._generate_dimensions(shape_analysis),
                'colors': self._process_colors(color_analysis),
                'materials': self._suggest_materials(texture_analysis),
                'details': self._generate_details(shape_analysis, texture_analysis)
            }
            
            logger.info(f"Successfully generated model parameters: {model_params['type']}")
            return model_params
        except Exception as e:
            logger.error(f"Error generating model parameters: {str(e)}")
            return {
                'type': 'basic_cube',
                'dimensions': {'width': 1.0, 'height': 1.0, 'depth': 1.0},
                'colors': [{'hex': '#CCCCCC', 'name': 'Gray'}],
                'materials': ['Plastic'],
                'details': []
            }
    
    def _determine_model_type(self, shape_analysis):
        """
        Determine the type of 3D model based on shape analysis.
        
        Args:
            shape_analysis (dict): Shape analysis results
            
        Returns:
            str: Model type
        """
        dominant_shapes = shape_analysis.get('dominant_shapes', ['Unknown'])
        
        if 'Circle' in dominant_shapes or 'Circular' in dominant_shapes:
            return 'cylindrical'
        elif 'Rectangle' in dominant_shapes or 'Square' in dominant_shapes:
            return 'box'
        elif 'Triangle' in dominant_shapes:
            return 'pyramid'
        elif 'Polygon' in dominant_shapes:
            return 'polyhedron'
        elif 'Organic' in dominant_shapes:
            return 'organic'
        else:
            return 'generic'
    
    def _generate_dimensions(self, shape_analysis):
        """
        Generate dimensions for the 3D model based on shape analysis.
        
        Args:
            shape_analysis (dict): Shape analysis results
            
        Returns:
            dict: Model dimensions
        """
        # Default dimensions
        dimensions = {
            'width': 1.0,
            'height': 1.0,
            'depth': 1.0
        }
        
        # Adjust dimensions based on shape analysis
        shapes = shape_analysis.get('shape_details', [])
        if shapes:
            # Find the largest shape by area
            largest_shape = max(shapes, key=lambda x: x.get('area', 0)) if shapes else {}
            
            # Get aspect ratio if available
            aspect_ratio = largest_shape.get('aspect_ratio', 1.0)
            
            # Adjust width and height based on aspect ratio
            if aspect_ratio > 1.0:
                dimensions['width'] = min(2.0, aspect_ratio)
                dimensions['height'] = 1.0
            else:
                dimensions['width'] = 1.0
                dimensions['height'] = min(2.0, 1.0 / aspect_ratio if aspect_ratio > 0 else 1.0)
            
            # Adjust depth based on shape type
            shape_type = largest_shape.get('type', '')
            if shape_type in ['Circle', 'Square']:
                dimensions['depth'] = dimensions['width']  # Make it more cube-like or cylindrical
            else:
                dimensions['depth'] = dimensions['width'] * 0.5  # Make it flatter
        
        return dimensions
    
    def _process_colors(self, color_analysis):
        """
        Process color analysis for the 3D model.
        
        Args:
            color_analysis (dict): Color analysis results
            
        Returns:
            list: Processed colors with names
        """
        processed_colors = []
        
        # Get hex colors from analysis
        hex_colors = color_analysis.get('hex_colors', [])
        
        # Define basic color mapping
        color_names = {
            '#FF0000': 'Red',
            '#00FF00': 'Green',
            '#0000FF': 'Blue',
            '#FFFF00': 'Yellow',
            '#FF00FF': 'Magenta',
            '#00FFFF': 'Cyan',
            '#000000': 'Black',
            '#FFFFFF': 'White',
            '#808080': 'Gray'
        }
        
        # Process each color
        for hex_color in hex_colors[:3]:  # Limit to top 3 colors
            # Find closest named color
            color_name = self._find_closest_color_name(hex_color, color_names)
            
            processed_colors.append({
                'hex': hex_color,
                'name': color_name
            })
        
        return processed_colors
    
    def _find_closest_color_name(self, hex_color, color_map):
        """
        Find the closest named color for a hex color.
        
        Args:
            hex_color (str): Hex color code
            color_map (dict): Mapping of hex colors to names
            
        Returns:
            str: Color name
        """
        if hex_color in color_map:
            return color_map[hex_color]
        
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Find closest color by RGB distance
        min_distance = float('inf')
        closest_name = 'Custom'
        
        for hex_code, name in color_map.items():
            hex_code = hex_code.lstrip('#')
            r2, g2, b2 = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
            
            # Calculate Euclidean distance in RGB space
            distance = ((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        return closest_name
    
    def _suggest_materials(self, texture_analysis):
        """
        Suggest materials based on texture analysis.
        
        Args:
            texture_analysis (dict): Texture analysis results
            
        Returns:
            list: Suggested materials
        """
        suggested_materials = []
        
        # Get texture properties
        texture_type = texture_analysis.get('texture_type', 'Unknown')
        roughness = texture_analysis.get('roughness', 0.0)
        pattern_type = texture_analysis.get('pattern_type', 'Unknown')
        
        # Suggest materials based on texture type
        if texture_type == 'Smooth':
            suggested_materials.extend(['Glass', 'Polished Metal', 'Plastic'])
        elif texture_type == 'Matte':
            suggested_materials.extend(['Matte Plastic', 'Rubber', 'Fabric'])
        elif texture_type == 'Rough':
            suggested_materials.extend(['Stone', 'Concrete', 'Wood'])
        elif texture_type == 'Textured':
            suggested_materials.extend(['Textured Plastic', 'Leather', 'Canvas'])
        else:
            suggested_materials.append('Plastic')  # Default material
        
        # Add additional materials based on pattern
        if pattern_type == 'Geometric':
            suggested_materials.append('3D Printed Polymer')
        elif pattern_type == 'Organic':
            suggested_materials.append('Natural Wood')
        
        return suggested_materials[:3]  # Limit to top 3 materials
    
    def _generate_details(self, shape_analysis, texture_analysis):
        """
        Generate details for the 3D model.
        
        Args:
            shape_analysis (dict): Shape analysis results
            texture_analysis (dict): Texture analysis results
            
        Returns:
            list: Model details
        """
        details = []
        
        # Add details based on shape complexity
        complexity = shape_analysis.get('shape_complexity', 'Low')
        if complexity == 'High':
            details.append({
                'type': 'surface_detail',
                'description': 'Complex surface patterns',
                'intensity': 0.8
            })
        elif complexity == 'Medium':
            details.append({
                'type': 'surface_detail',
                'description': 'Moderate surface patterns',
                'intensity': 0.5
            })
        
        # Add details based on texture
        texture_type = texture_analysis.get('texture_type', 'Unknown')
        if texture_type == 'Rough':
            details.append({
                'type': 'roughness',
                'description': 'Rough surface texture',
                'intensity': 0.7
            })
        elif texture_type == 'Textured':
            details.append({
                'type': 'bump_map',
                'description': 'Textured surface',
                'intensity': 0.6
            })
        
        # Add details based on pattern
        pattern_type = texture_analysis.get('pattern_type', 'Unknown')
        if pattern_type == 'Geometric':
            details.append({
                'type': 'geometric_pattern',
                'description': 'Geometric surface pattern',
                'intensity': 0.5
            })
        elif pattern_type == 'Organic':
            details.append({
                'type': 'organic_pattern',
                'description': 'Organic surface pattern',
                'intensity': 0.6
            })
        
        return details
    
    def generate_model_file(self, model_params, output_dir, filename='model_params.json'):
        """
        Generate a model parameter file that can be used to create a 3D model.
        
        Args:
            model_params (dict): Model parameters
            output_dir (str): Directory to save the model file
            filename (str): Name of the model file
            
        Returns:
            str: Path to the generated model file
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output path
            output_path = os.path.join(output_dir, filename)
            
            # Save model parameters as JSON
            with open(output_path, 'w') as f:
                json.dump(model_params, f, indent=2)
            
            logger.info(f"Model parameters saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving model parameters: {str(e)}")
            return None


if __name__ == "__main__":
    # Example usage
    generator = ModelGenerator()
    
    # Test with a sample image if available
    test_image = "sample.jpg"  # Replace with an actual image path for testing
    if os.path.exists(test_image):
        # Mock analysis results for testing
        shape_analysis = {
            'dominant_shapes': ['Rectangle', 'Circle'],
            'shape_complexity': 'Medium',
            'shape_details': [
                {'type': 'Rectangle', 'area': 10000, 'aspect_ratio': 1.5}
            ]
        }
        
        color_analysis = {
            'hex_colors': ['#3F51B5', '#F44336', '#4CAF50']
        }
        
        texture_analysis = {
            'texture_type': 'Smooth',
            'roughness': 5.0,
            'pattern_type': 'Geometric'
        }
        
        # Generate model parameters
        model_params = generator.generate_model_parameters(
            test_image, shape_analysis, color_analysis, texture_analysis
        )
        
        print("Model parameters:", model_params)
        
        # Save model parameters
        generator.generate_model_file(model_params, "./output")
