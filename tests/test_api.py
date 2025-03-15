import unittest
import sys
import os
import json

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import API app for testing
from backend.api.app import app

class APITestCase(unittest.TestCase):
    """Test case for the API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data['services']['image_recognition'])
        self.assertTrue(data['services']['nlp'])
        self.assertTrue(data['services']['design_engine'])
    
    def test_process_command(self):
        """Test process command endpoint"""
        command_data = {
            'command': 'Create a modern chair design with sustainable materials'
        }
        
        response = self.app.post('/api/process-command', 
                                json=command_data,
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('command_data' in data)
        self.assertTrue('message' in data)
    
    def test_create_project(self):
        """Test create project endpoint"""
        project_data = {
            'name': 'Test Project',
            'industry': 'furniture',
            'description': 'A test project for unit testing'
        }
        
        response = self.app.post('/api/projects', 
                                json=project_data,
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('project_id' in data)
        self.assertEqual(data['project']['name'], 'Test Project')
        self.assertEqual(data['project']['industry'], 'furniture')
    
    def test_get_materials(self):
        """Test get materials endpoint"""
        response = self.app.get('/api/materials')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('materials' in data)
    
    def test_get_standards(self):
        """Test get standards endpoint"""
        response = self.app.get('/api/standards')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('standards' in data)
    
    def test_get_templates(self):
        """Test get templates endpoint"""
        response = self.app.get('/api/templates')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('templates' in data)
    
    def test_get_trends(self):
        """Test get trends endpoint"""
        response = self.app.get('/api/trends')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('trends' in data)
    
    def test_create_collaboration_session(self):
        """Test create collaboration session endpoint"""
        # First create a project
        project_data = {
            'name': 'Collaboration Test Project',
            'industry': 'furniture',
            'description': 'A test project for collaboration testing'
        }
        
        project_response = self.app.post('/api/projects', 
                                        json=project_data,
                                        content_type='application/json')
        project_data = json.loads(project_response.data)
        project_id = project_data['project_id']
        
        # Now create a collaboration session
        session_data = {
            'project_id': project_id,
            'name': 'Test Collaboration Session'
        }
        
        response = self.app.post('/api/collaboration/sessions', 
                                json=session_data,
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('session_id' in data)
        self.assertEqual(data['name'], 'Test Collaboration Session')
        self.assertEqual(data['project_id'], project_id)

if __name__ == '__main__':
    unittest.main()
