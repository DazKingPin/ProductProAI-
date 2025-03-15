from flask import Flask, request, jsonify
import os
import sys
import logging
import json
from werkzeug.utils import secure_filename
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import services
from services.image_recognition.image_analyzer import ImageAnalyzer
from services.nlp.text_processor import TextProcessor
from services.nlp.intent_classifier import IntentClassifier
from services.nlp.entity_extractor import EntityExtractor
from services.nlp.command_parser import CommandParser
from services.nlp.response_generator import ResponseGenerator
from services.design_engine.design_manager import DesignManager
from services.design_engine.material_database import MaterialDatabase
from services.design_engine.industry_standards import IndustryStandards
from services.design_engine.sustainability_analyzer import SustainabilityAnalyzer
from services.design_engine.trend_analyzer import TrendAnalyzer
from services.design_engine.compliance_checker import ComplianceChecker

# Create Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Initialize services
image_analyzer = ImageAnalyzer()
text_processor = TextProcessor()
intent_classifier = IntentClassifier()
entity_extractor = EntityExtractor()
command_parser = CommandParser(intent_classifier, entity_extractor)
response_generator = ResponseGenerator()

# Initialize design engine services
material_database = MaterialDatabase()
industry_standards = IndustryStandards()
sustainability_analyzer = SustainabilityAnalyzer()
trend_analyzer = TrendAnalyzer()
compliance_checker = ComplianceChecker()

# Initialize design manager with all services
design_manager = DesignManager(
    material_service=material_database,
    standards_service=industry_standards,
    sustainability_service=sustainability_analyzer,
    trend_service=trend_analyzer,
    compliance_service=compliance_checker,
    database_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'design_database.json')
)

# Create data directory if it doesn't exist
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'), exist_ok=True)

# Ensure design database is saved
design_manager.save_database()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'image_recognition': True,
            'nlp': True,
            'design_engine': True
        }
    })

@app.route('/api/process-command', methods=['POST'])
def process_command():
    """Process a text command"""
    try:
        data = request.json
        if not data or 'command' not in data:
            return jsonify({'error': 'Missing command text'}), 400
        
        command_text = data.get('command')
        project_id = data.get('project_id')
        
        # Process command text
        processed_text = text_processor.process_text(command_text)
        
        # Parse command
        command_data = command_parser.parse_command(processed_text)
        
        # Process design command if project_id is provided
        if project_id:
            result = design_manager.process_design_command(project_id, command_data)
            
            # Generate response
            response_text = response_generator.generate_response(command_data, result)
            
            return jsonify({
                'success': result.get('success', False),
                'message': response_text,
                'command_data': command_data,
                'result': result
            })
        else:
            # Generate general response
            response_text = response_generator.generate_response(command_data)
            
            return jsonify({
                'success': True,
                'message': response_text,
                'command_data': command_data
            })
    
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Upload and analyze an image"""
    try:
        # Check if the post request has the file part
        if 'image' not in request.files:
            return jsonify({'error': 'No image part'}), 400
        
        file = request.files['image']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Get project ID if provided
        project_id = request.form.get('project_id')
        
        if file:
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save the file
            file.save(file_path)
            
            # Analyze the image
            analysis_results = image_analyzer.analyze_image(file_path)
            
            # If project_id is provided, update the project with the image analysis
            if project_id:
                design_manager.analyze_reference_image(project_id, file_path)
            
            return jsonify({
                'success': True,
                'file_path': file_path,
                'analysis': analysis_results
            })
    
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all design projects"""
    try:
        projects = design_manager.design_projects
        return jsonify({
            'success': True,
            'projects': projects
        })
    
    except Exception as e:
        logger.error(f"Error getting projects: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new design project"""
    try:
        data = request.json
        if not data or 'name' not in data or 'industry' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        name = data.get('name')
        industry = data.get('industry')
        template_id = data.get('template_id')
        reference_image = data.get('reference_image')
        description = data.get('description')
        
        project_id = design_manager.create_design_project(
            name=name,
            industry=industry,
            template_id=template_id,
            reference_image=reference_image,
            description=description
        )
        
        if project_id:
            # Save database
            design_manager.save_database()
            
            return jsonify({
                'success': True,
                'project_id': project_id,
                'project': design_manager.get_design_project(project_id)
            })
        else:
            return jsonify({'error': 'Failed to create project'}), 500
    
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific design project"""
    try:
        project = design_manager.get_design_project(project_id)
        if project:
            return jsonify({
                'success': True,
                'project': project
            })
        else:
            return jsonify({'error': 'Project not found'}), 404
    
    except Exception as e:
        logger.error(f"Error getting project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a design project"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Missing update data'}), 400
        
        success = design_manager.update_design_project(project_id, data)
        
        if success:
            # Save database
            design_manager.save_database()
            
            return jsonify({
                'success': True,
                'project': design_manager.get_design_project(project_id)
            })
        else:
            return jsonify({'error': 'Failed to update project'}), 500
    
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a design project"""
    try:
        success = design_manager.delete_design_project(project_id)
        
        if success:
            # Save database
            design_manager.save_database()
            
            return jsonify({
                'success': True,
                'message': f"Project {project_id} deleted"
            })
        else:
            return jsonify({'error': 'Failed to delete project'}), 500
    
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>/analyze', methods=['POST'])
def analyze_project(project_id):
    """Analyze a design project"""
    try:
        analysis_results = design_manager.analyze_design(project_id)
        
        if 'error' not in analysis_results:
            # Save database
            design_manager.save_database()
            
            return jsonify({
                'success': True,
                'analysis': analysis_results
            })
        else:
            return jsonify({'error': analysis_results.get('error')}), 500
    
    except Exception as e:
        logger.error(f"Error analyzing project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>/recommendations', methods=['GET'])
def get_recommendations(project_id):
    """Get recommendations for a design project"""
    try:
        recommendations = design_manager.generate_design_recommendations(project_id)
        
        if 'error' not in recommendations:
            return jsonify({
                'success': True,
                'recommendations': recommendations
            })
        else:
            return jsonify({'error': recommendations.get('error')}), 500
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>/visualization', methods=['GET'])
def get_visualization(project_id):
    """Get visualization data for a design project"""
    try:
        visualization = design_manager.generate_design_visualization(project_id)
        
        if 'error' not in visualization:
            return jsonify({
                'success': True,
                'visualization': visualization
            })
        else:
            return jsonify({'error': visualization.get('error')}), 500
    
    except Exception as e:
        logger.error(f"Error getting visualization: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>/export', methods=['GET'])
def export_project(project_id):
    """Export design data for a project"""
    try:
        format = request.args.get('format', 'json')
        export_data = design_manager.export_design_data(project_id, format=format)
        
        if 'error' not in export_data:
            return jsonify({
                'success': True,
                'export_data': export_data
            })
        else:
            return jsonify({'error': export_data.get('error')}), 500
    
    except Exception as e:
        logger.error(f"Error exporting project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/materials', methods=['GET'])
def get_materials():
    """Get all materials"""
    try:
        category = request.args.get('category')
        materials = material_database.get_all_materials(category=category)
        
        return jsonify({
            'success': True,
            'materials': materials
        })
    
    except Exception as e:
        logger.error(f"Error getting materials: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/materials/<material_id>', methods=['GET'])
def get_material(material_id):
    """Get a specific material"""
    try:
        material = material_database.get_material(material_id)
        
        if material:
            return jsonify({
                'success': True,
                'material': material
            })
        else:
            return jsonify({'error': 'Material not found'}), 404
    
    except Exception as e:
        logger.error(f"Error getting material: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/standards', methods=['GET'])
def get_standards():
    """Get all industry standards"""
    try:
        industry = request.args.get('industry')
        standards = industry_standards.get_all_standards(industry=industry)
        
        return jsonify({
            'success': True,
            'standards': standards
        })
    
    except Exception as e:
        logger.error(f"Error getting standards: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/standards/<standard_id>', methods=['GET'])
def get_standard(standard_id):
    """Get a specific industry standard"""
    try:
        standard = industry_standards.get_standard(standard_id)
        
        if standard:
            return jsonify({
                'success': True,
                'standard': standard
            })
        else:
            return jsonify({'error': 'Standard not found'}), 404
    
    except Exception as e:
        logger.error(f"Error getting standard: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get design templates"""
    try:
        industry = request.args.get('industry')
        
        if industry:
            templates = design_manager.get_industry_templates(industry)
        else:
            templates = design_manager.design_templates
        
        return jsonify({
            'success': True,
            'templates': templates
        })
    
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates/<industry>/<template_id>', methods=['GET'])
def get_template(industry, template_id):
    """Get a specific design template"""
    try:
        template = design_manager.get_template(industry, template_id)
        
        if template:
            return jsonify({
                'success': True,
                'template': template
            })
        else:
            return jsonify({'error': 'Template not found'}), 404
    
    except Exception as e:
        logger.error(f"Error getting template: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/industry-configs', methods=['GET'])
def get_industry_configs():
    """Get industry configurations"""
    try:
        industry = request.args.get('industry')
        
        if industry:
            config = design_manager.get_industry_config(industry)
            configs = {industry: config} if config else {}
        else:
            configs = design_manager.industry_configs
        
        return jsonify({
            'success': True,
            'configs': configs
        })
    
    except Exception as e:
        logger.error(f"Error getting industry configs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get market trends"""
    try:
        industry = request.args.get('industry')
        trends = trend_analyzer.get_trends(industry=industry)
        
        return jsonify({
            'success': True,
            'trends': trends
        })
    
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sustainability/materials', methods=['GET'])
def get_sustainable_materials():
    """Get sustainable materials"""
    try:
        category = request.args.get('category')
        min_score = request.args.get('min_score')
        
        if min_score:
            try:
                min_score = float(min_score)
            except ValueError:
                min_score = None
        
        materials = sustainability_analyzer.get_sustainable_materials(
            category=category,
            min_score=min_score
        )
        
        return jsonify({
            'success': True,
            'materials': materials
        })
    
    except Exception as e:
        logger.error(f"Error getting sustainable materials: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/collaboration/sessions', methods=['POST'])
def create_collaboration_session():
    """Create a new collaboration session"""
    try:
        data = request.json
        if not data or 'project_id' not in data:
            return jsonify({'error': 'Missing project_id'}), 400
        
        project_id = data.get('project_id')
        name = data.get('name', f"Collaboration on {project_id}")
        
        # In a real implementation, this would create a collaboration session
        # For now, we'll just return a mock session ID
        session_id = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'name': name,
            'project_id': project_id,
            'created_at': str(uuid.uuid1()),
            'status': 'active'
        })
    
    except Exception as e:
        logger.error(f"Error creating collaboration session: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Run the app if executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
