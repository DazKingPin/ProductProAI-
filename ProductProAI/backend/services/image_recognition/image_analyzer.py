import os
import logging
import json
from .color_extractor import ColorExtractor
from .texture_analyzer import TextureAnalyzer
from .shape_detector import ShapeDetector
from .model_generator import ModelGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """
    Main class for analyzing images and generating product design suggestions.
    Integrates color extraction, texture analysis, shape detection, and 3D model generation.
    """
    
    def __init__(self, output_dir="./output"):
        """
        Initialize the ImageAnalyzer.
        
        Args:
            output_dir (str): Directory to save output files
        """
        logger.info("Initializing ImageAnalyzer")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.color_extractor = ColorExtractor(n_colors=5)
        self.texture_analyzer = TextureAnalyzer()
        self.shape_detector = ShapeDetector()
        self.model_generator = ModelGenerator()
        
        logger.info("ImageAnalyzer initialized successfully")
    
    def analyze_image(self, image_path, generate_visualizations=True):
        """
        Analyze an image and generate comprehensive analysis results.
        
        Args:
            image_path (str): Path to the image file
            generate_visualizations (bool): Whether to generate visualization files
            
        Returns:
            dict: Comprehensive analysis results
        """
        try:
            logger.info(f"Starting analysis of image: {image_path}")
            
            # Check if image exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Create output directory for this image
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            image_output_dir = os.path.join(self.output_dir, file_name)
            os.makedirs(image_output_dir, exist_ok=True)
            
            # Extract colors
            logger.info("Extracting colors")
            color_palette = self.color_extractor.get_color_palette(
                image_path, 
                save_visualization=generate_visualizations,
                output_dir=image_output_dir
            )
            
            # Analyze texture
            logger.info("Analyzing texture")
            texture_analysis = self.texture_analyzer.analyze_texture(image_path)
            
            if generate_visualizations:
                self.texture_analyzer.save_texture_visualization(image_path, image_output_dir)
            
            # Detect shapes
            logger.info("Detecting shapes")
            shape_analysis = self.shape_detector.detect_shapes(image_path)
            
            if generate_visualizations:
                self.shape_detector.save_shape_visualization(image_path, image_output_dir)
            
            # Generate model parameters
            logger.info("Generating model parameters")
            model_params = self.model_generator.generate_model_parameters(
                image_path, shape_analysis, color_palette, texture_analysis
            )
            
            # Save model parameters
            model_file = self.model_generator.generate_model_file(
                model_params, 
                image_output_dir, 
                filename=f"{file_name}_model.json"
            )
            
            # Compile comprehensive analysis results
            analysis_results = {
                'image_path': image_path,
                'color_analysis': color_palette,
                'texture_analysis': texture_analysis,
                'shape_analysis': shape_analysis,
                'model_parameters': model_params,
                'output_directory': image_output_dir,
                'visualization_files': self._get_visualization_files(image_output_dir) if generate_visualizations else []
            }
            
            # Save comprehensive analysis results
            self._save_analysis_results(analysis_results, image_output_dir, file_name)
            
            logger.info(f"Image analysis completed successfully for {image_path}")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            return {
                'error': str(e),
                'image_path': image_path,
                'status': 'failed'
            }
    
    def _get_visualization_files(self, directory):
        """
        Get list of visualization files in the output directory.
        
        Args:
            directory (str): Directory to search for visualization files
            
        Returns:
            list: Paths to visualization files
        """
        visualization_files = []
        
        for file in os.listdir(directory):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                visualization_files.append(os.path.join(directory, file))
        
        return visualization_files
    
    def _save_analysis_results(self, analysis_results, output_dir, file_name):
        """
        Save analysis results to a JSON file.
        
        Args:
            analysis_results (dict): Analysis results
            output_dir (str): Directory to save the results
            file_name (str): Base name for the output file
            
        Returns:
            str: Path to the saved file
        """
        try:
            # Create a simplified version of the results for JSON serialization
            serializable_results = {
                'image_path': analysis_results['image_path'],
                'color_analysis': {
                    'dominant_colors': analysis_results['color_analysis']['hex_colors'],
                    'percentages': [float(p) for p in analysis_results['color_analysis']['percentages']]
                },
                'texture_analysis': {
                    'texture_type': analysis_results['texture_analysis']['texture_type'],
                    'roughness': float(analysis_results['texture_analysis']['roughness']),
                    'pattern_type': analysis_results['texture_analysis']['pattern_type']
                },
                'shape_analysis': {
                    'dominant_shapes': analysis_results['shape_analysis']['dominant_shapes'],
                    'shape_complexity': analysis_results['shape_analysis']['shape_complexity']
                },
                'model_parameters': analysis_results['model_parameters'],
                'output_directory': analysis_results['output_directory'],
                'visualization_files': analysis_results['visualization_files']
            }
            
            # Save to JSON file
            output_path = os.path.join(output_dir, f"{file_name}_analysis.json")
            with open(output_path, 'w') as f:
                json.dump(serializable_results, f, indent=2)
            
            logger.info(f"Analysis results saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving analysis results: {str(e)}")
            return None
    
    def generate_design_suggestions(self, analysis_results):
        """
        Generate design suggestions based on image analysis.
        
        Args:
            analysis_results (dict): Image analysis results
            
        Returns:
            dict: Design suggestions
        """
        try:
            logger.info("Generating design suggestions")
            
            # Extract key information from analysis results
            dominant_colors = analysis_results['color_analysis']['hex_colors']
            texture_type = analysis_results['texture_analysis']['texture_type']
            dominant_shapes = analysis_results['shape_analysis']['dominant_shapes']
            model_type = analysis_results['model_parameters']['type']
            suggested_materials = analysis_results['model_parameters']['materials']
            
            # Generate color suggestions
            color_suggestions = self._generate_color_suggestions(dominant_colors)
            
            # Generate material suggestions
            material_suggestions = self._generate_material_suggestions(texture_type, suggested_materials)
            
            # Generate form suggestions
            form_suggestions = self._generate_form_suggestions(dominant_shapes, model_type)
            
            # Compile design suggestions
            design_suggestions = {
                'color_suggestions': color_suggestions,
                'material_suggestions': material_suggestions,
                'form_suggestions': form_suggestions,
                'design_approach': self._determine_design_approach(analysis_results)
            }
            
            logger.info("Design suggestions generated successfully")
            return design_suggestions
            
        except Exception as e:
            logger.error(f"Error generating design suggestions: {str(e)}")
            return {
                'color_suggestions': [],
                'material_suggestions': [],
                'form_suggestions': [],
                'design_approach': 'Balanced'
            }
    
    def _generate_color_suggestions(self, dominant_colors):
        """
        Generate color suggestions based on dominant colors.
        
        Args:
            dominant_colors (list): List of dominant colors in hex format
            
        Returns:
            dict: Color suggestions
        """
        # Use only the top 3 colors
        top_colors = dominant_colors[:3] if dominant_colors else ['#CCCCCC']
        
        # Generate complementary colors
        complementary_colors = []
        for color in top_colors:
            # Convert hex to RGB
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
            # Generate complementary color (simple RGB inversion)
            comp_r, comp_g, comp_b = 255 - r, 255 - g, 255 - b
            comp_color = f'#{comp_r:02x}{comp_g:02x}{comp_b:02x}'
            complementary_colors.append(comp_color)
        
        return {
            'primary_palette': top_colors,
            'complementary_palette': complementary_colors,
            'recommended_accent': complementary_colors[0] if complementary_colors else '#FF5722'
        }
    
    def _generate_material_suggestions(self, texture_type, suggested_materials):
        """
        Generate material suggestions based on texture analysis.
        
        Args:
            texture_type (str): Detected texture type
            suggested_materials (list): Materials suggested by model generator
            
        Returns:
            dict: Material suggestions
        """
        # Define sustainable alternatives for common materials
        sustainable_alternatives = {
            'Plastic': 'Recycled Plastic',
            'Glass': 'Recycled Glass',
            'Metal': 'Recycled Aluminum',
            'Wood': 'FSC-Certified Wood',
            'Leather': 'Vegan Leather',
            'Fabric': 'Organic Cotton'
        }
        
        # Generate eco-friendly alternatives
        eco_friendly = []
        for material in suggested_materials:
            for key, value in sustainable_alternatives.items():
                if key in material:
                    eco_friendly.append(value)
                    break
            else:
                eco_friendly.append('Sustainable ' + material)
        
        return {
            'recommended_materials': suggested_materials,
            'eco_friendly_alternatives': eco_friendly,
            'texture_recommendation': f"{texture_type} finish"
        }
    
    def _generate_form_suggestions(self, dominant_shapes, model_type):
        """
        Generate form suggestions based on shape analysis.
        
        Args:
            dominant_shapes (list): List of dominant shapes
            model_type (str): Type of 3D model
            
        Returns:
            dict: Form suggestions
        """
        # Define form suggestions based on shape and model type
        form_description = "Balanced form with "
        
        if 'Circle' in dominant_shapes or 'Circular' in dominant_shapes:
            form_description += "curved elements and organic flow"
        elif 'Rectangle' in dominant_shapes or 'Square' in dominant_shapes:
            form_description += "clean lines and structured geometry"
        elif 'Triangle' in dominant_shapes:
            form_description += "dynamic angles and directional elements"
        elif 'Organic' in dominant_shapes:
            form_description += "natural, flowing contours"
        else:
            form_description += "mixed geometric elements"
        
        return {
            'form_description': form_description,
            'recommended_proportions': self._get_recommended_proportions(model_type),
            'ergonomic_considerations': self._get_ergonomic_considerations(model_type)
        }
    
    def _get_recommended_proportions(self, model_type):
        """
        Get recommended proportions based on model type.
        
        Args:
            model_type (str): Type of 3D model
            
        Returns:
            str: Recommended proportions
        """
        if model_type == 'cylindrical':
            return "Golden ratio (1:1.618) for height to diameter"
        elif model_type == 'box':
            return "Rule of thirds for dividing surfaces"
        elif model_type == 'pyramid':
            return "Balanced base-to-height ratio of 2:1"
        elif model_type == 'organic':
            return "Asymmetrical balance with focal point"
        else:
            return "Balanced proportions with visual hierarchy"
    
    def _get_ergonomic_considerations(self, model_type):
        """
        Get ergonomic considerations based on model type.
        
        Args:
            model_type (str): Type of 3D model
            
        Returns:
            list: Ergonomic considerations
        """
        common_considerations = ["Consider user comfort and accessibility"]
        
        if model_type == 'cylindrical':
            return common_considerations + ["Ensure comfortable grip diameter", "Round edges for hand comfort"]
        elif model_type == 'box':
            return common_considerations + ["Avoid sharp corners", "Consider weight distribution"]
        elif model_type == 'organic':
            return common_considerations + ["Follow natural hand/body contours", "Test with diverse user groups"]
        else:
            return common_considerations + ["Balance aesthetics with usability", "Consider user interaction points"]
    
    def _determine_design_approach(self, analysis_results):
        """
        Determine overall design approach based on analysis results.
        
        Args:
            analysis_results (dict): Image analysis results
            
        Returns:
            str: Recommended design approach
        """
        # Extract key information
        texture_type = analysis_results['texture_analysis']['texture_type']
        shape_complexity = analysis_results['shape_analysis']['shape_complexity']
        
        # Determine approach based on texture and shape complexity
        if texture_type in ['Smooth', 'Matte'] and shape_complexity == 'Low':
            return "Minimalist"
        elif texture_type in ['Textured', 'Rough'] and shape_complexity == 'High':
            return "Organic/Natural"
        elif 'Geometric' in str(analysis_results['shape_analysis']['dominant_shapes']):
            return "Geometric/Structured"
        elif texture_type == 'Smooth' and shape_complexity == 'High':
            return "Modern/Sleek"
        else:
            return "Balanced"


if __name__ == "__main__":
    # Example usage
    analyzer = ImageAnalyzer(output_dir="./output")
    
    # Test with a sample image if available
    test_image = "sample.jpg"  # Replace with an actual image path for testing
    if os.path.exists(test_image):
        # Analyze image
        analysis_results = analyzer.analyze_image(test_image)
        
        # Generate design suggestions
        if 'error' not in analysis_results:
            design_suggestions = analyzer.generate_design_suggestions(analysis_results)
            print("Design suggestions:", design_suggestions)
