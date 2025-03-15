import unittest
import sys
import os

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import NLP components for testing
from backend.services.nlp.text_processor import TextProcessor
from backend.services.nlp.intent_classifier import IntentClassifier
from backend.services.nlp.entity_extractor import EntityExtractor
from backend.services.nlp.command_parser import CommandParser
from backend.services.nlp.response_generator import ResponseGenerator

class NLPTestCase(unittest.TestCase):
    """Test case for the NLP components"""
    
    def setUp(self):
        """Set up test objects"""
        self.text_processor = TextProcessor()
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.command_parser = CommandParser(self.intent_classifier, self.entity_extractor)
        self.response_generator = ResponseGenerator()
    
    def test_text_processor_initialization(self):
        """Test text processor initialization"""
        self.assertIsNotNone(self.text_processor)
    
    def test_intent_classifier_initialization(self):
        """Test intent classifier initialization"""
        self.assertIsNotNone(self.intent_classifier)
    
    def test_entity_extractor_initialization(self):
        """Test entity extractor initialization"""
        self.assertIsNotNone(self.entity_extractor)
    
    def test_command_parser_initialization(self):
        """Test command parser initialization"""
        self.assertIsNotNone(self.command_parser)
    
    def test_response_generator_initialization(self):
        """Test response generator initialization"""
        self.assertIsNotNone(self.response_generator)
    
    def test_text_processing(self):
        """Test text processing functionality"""
        # Test basic text processing
        test_text = "Create a modern chair design with sustainable materials"
        processed_text = self.text_processor.process_text(test_text)
        self.assertIsNotNone(processed_text)
    
    def test_command_parsing(self):
        """Test command parsing functionality"""
        # Test basic command parsing
        test_text = "Create a modern chair design with sustainable materials"
        processed_text = self.text_processor.process_text(test_text)
        command_data = self.command_parser.parse_command(processed_text)
        
        self.assertIsNotNone(command_data)
        self.assertTrue('intent' in command_data)
        self.assertTrue('entities' in command_data)

if __name__ == '__main__':
    unittest.main()
