import unittest
import sys
import os

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import design engine components for testing
from backend.services.design_engine.design_manager import DesignManager
from backend.services.design_engine.material_database import MaterialDatabase
from backend.services.design_engine.industry_standards import IndustryStandards
from backend.services.design_engine.sustainability_analyzer import SustainabilityAnalyzer
from backend.services.design_engine.trend_analyzer import TrendAnalyzer
from backend.services.design_engine.compliance_checker import ComplianceChecker

class DesignEngineTestCase(unittest.TestCase):
    """Test case for the design engine components"""
    
    def setUp(self):
        """Set up test objects"""
        self.material_database = MaterialDatabase()
        self.industry_standards = IndustryStandards()
        self.sustainability_analyzer = SustainabilityAnalyzer()
        self.trend_analyzer = TrendAnalyzer()
        self.compliance_checker = ComplianceChecker()
        
        # Initialize design manager with all services
        self.design_manager = DesignManager(
            material_service=self.material_database,
            standards_service=self.industry_standards,
            sustainability_service=self.sustainability_analyzer,
            trend_service=self.trend_analyzer,
            compliance_service=self.compliance_checker
        )
    
    def test_material_database_initialization(self):
        """Test material database initialization"""
        self.assertIsNotNone(self.material_database)
    
    def test_industry_standards_initialization(self):
        """Test industry standards initialization"""
        self.assertIsNotNone(self.industry_standards)
    
    def test_sustainability_analyzer_initialization(self):
        """Test sustainability analyzer initialization"""
        self.assertIsNotNone(self.sustainability_analyzer)
    
    def test_trend_analyzer_initialization(self):
        """Test trend analyzer initialization"""
        self.assertIsNotNone(self.trend_analyzer)
    
    def test_compliance_checker_initialization(self):
        """Test compliance checker initialization"""
        self.assertIsNotNone(self.compliance_checker)
    
    def test_design_manager_initialization(self):
        """Test design manager initialization"""
        self.assertIsNotNone(self.design_manager)
    
    def test_design_project_creation(self):
        """Test design project creation"""
        project_id = self.design_manager.create_design_project(
            name="Test Chair",
            industry="furniture",
            description="A test chair design"
        )
        
        self.assertIsNotNone(project_id)
        
        # Verify project was created
        project = self.design_manager.get_design_project(project_id)
        self.assertIsNotNone(project)
        self.assertEqual(project['name'], "Test Chair")
        self.assertEqual(project['industry'], "furniture")
    
    def test_design_template_access(self):
        """Test design template access"""
        # Get templates for furniture industry
        furniture_templates = self.design_manager.get_industry_templates('furniture')
        self.assertIsNotNone(furniture_templates)
        
        # There should be at least one template
        self.assertGreater(len(furniture_templates), 0)
    
    def test_industry_config_access(self):
        """Test industry configuration access"""
        # Get configuration for furniture industry
        furniture_config = self.design_manager.get_industry_config('furniture')
        self.assertIsNotNone(furniture_config)
        
        # Verify configuration has expected fields
        self.assertTrue('name' in furniture_config)
        self.assertTrue('design_principles' in furniture_config)

if __name__ == '__main__':
    unittest.main()
