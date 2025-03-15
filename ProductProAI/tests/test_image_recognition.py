import unittest
import sys
import os

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import image recognition components for testing
from backend.services.image_recognition.color_extractor import ColorExtractor
from backend.services.image_recognition.texture_analyzer import TextureAnalyzer
from backend.services.image_recognition.shape_detector import ShapeDetector
from backend.services.image_recognition.image_analyzer import ImageAnalyzer

class ImageRecognitionTestCase(unittest.TestCase):
    """Test case for the image recognition components"""
    
    def setUp(self):
        """Set up test objects"""
        self.color_extractor = ColorExtractor()
        self.texture_analyzer = TextureAnalyzer()
        self.shape_detector = ShapeDetector()
        self.image_analyzer = ImageAnalyzer()
    
    def test_color_extractor_initialization(self):
        """Test color extractor initialization"""
        self.assertIsNotNone(self.color_extractor)
    
    def test_texture_analyzer_initialization(self):
        """Test texture analyzer initialization"""
        self.assertIsNotNone(self.texture_analyzer)
    
    def test_shape_detector_initialization(self):
        """Test shape detector initialization"""
        self.assertIsNotNone(self.shape_detector)
    
    def test_image_analyzer_initialization(self):
        """Test image analyzer initialization"""
        self.assertIsNotNone(self.image_analyzer)
    
    def test_image_analyzer_methods(self):
        """Test image analyzer methods"""
        # Check that the analyze_image method exists
        self.assertTrue(hasattr(self.image_analyzer, 'analyze_image'))
        self.assertTrue(callable(getattr(self.image_analyzer, 'analyze_image')))

if __name__ == '__main__':
    unittest.main()
