import logging
import json
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SustainabilityAnalyzer:
    """
    Class for analyzing and optimizing product designs for sustainability.
    Provides eco-friendly design recommendations and sustainability metrics.
    """
    
    def __init__(self, database_path=None):
        """
        Initialize the SustainabilityAnalyzer.
        
        Args:
            database_path (str, optional): Path to the sustainability database file
        """
        logger.info("Initializing SustainabilityAnalyzer")
        self.database_path = database_path
        self.sustainability_data = {}
        self.materials_impact = {}
        self.manufacturing_impact = {}
        self.lifecycle_factors = {}
        self._load_sustainability_data()
    
    def _load_sustainability_data(self):
        """
        Load sustainability data from database file or initialize with default data.
        """
        try:
            if self.database_path and os.path.exists(self.database_path):
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    self.sustainability_data = data.get('sustainability_data', {})
                    self.materials_impact = data.get('materials_impact', {})
                    self.manufacturing_impact = data.get('manufacturing_impact', {})
                    self.lifecycle_factors = data.get('lifecycle_factors', {})
                logger.info(f"Loaded sustainability data from database")
            else:
                logger.info("Initializing default sustainability database")
                self._initialize_default_data()
        except Exception as e:
            logger.error(f"Error loading sustainability data: {str(e)}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """
        Initialize the database with default sustainability data.
        """
        # Initialize materials environmental impact data
        self.materials_impact = {
            'aluminum': {
                'carbon_footprint': 8.24,  # kg CO2e per kg
                'water_usage': 97.0,  # liters per kg
                'energy_consumption': 155.0,  # MJ per kg
                'recyclability': 0.95,  # 0-1 scale
                'biodegradability': 0.0,  # 0-1 scale
                'toxicity': 0.2,  # 0-1 scale
                'resource_depletion': 0.6  # 0-1 scale
            },
            'steel': {
                'carbon_footprint': 1.85,  # kg CO2e per kg
                'water_usage': 28.5,  # liters per kg
                'energy_consumption': 25.0,  # MJ per kg
                'recyclability': 0.98,  # 0-1 scale
                'biodegradability': 0.0,  # 0-1 scale
                'toxicity': 0.15,  # 0-1 scale
                'resource_depletion': 0.4  # 0-1 scale
            },
            'abs_plastic': {
                'carbon_footprint': 3.45,  # kg CO2e per kg
                'water_usage': 125.0,  # liters per kg
                'energy_consumption': 95.0,  # MJ per kg
                'recyclability': 0.6,  # 0-1 scale
                'biodegradability': 0.05,  # 0-1 scale
                'toxicity': 0.4,  # 0-1 scale
                'resource_depletion': 0.7  # 0-1 scale
            },
            'polypropylene': {
                'carbon_footprint': 2.0,  # kg CO2e per kg
                'water_usage': 52.0,  # liters per kg
                'energy_consumption': 73.0,  # MJ per kg
                'recyclability': 0.7,  # 0-1 scale
                'biodegradability': 0.1,  # 0-1 scale
                'toxicity': 0.25,  # 0-1 scale
                'resource_depletion': 0.65  # 0-1 scale
            },
            'oak': {
                'carbon_footprint': 0.45,  # kg CO2e per kg
                'water_usage': 15.0,  # liters per kg
                'energy_consumption': 10.0,  # MJ per kg
                'recyclability': 0.8,  # 0-1 scale
                'biodegradability': 0.95,  # 0-1 scale
                'toxicity': 0.05,  # 0-1 scale
                'resource_depletion': 0.3  # 0-1 scale
            },
            'bamboo': {
                'carbon_footprint': 0.25,  # kg CO2e per kg
                'water_usage': 8.0,  # liters per kg
                'energy_consumption': 5.0,  # MJ per kg
                'recyclability': 0.85,  # 0-1 scale
                'biodegradability': 0.98,  # 0-1 scale
                'toxicity': 0.02,  # 0-1 scale
                'resource_depletion': 0.1  # 0-1 scale
            },
            'cotton': {
                'carbon_footprint': 5.89,  # kg CO2e per kg
                'water_usage': 10000.0,  # liters per kg (very high water usage)
                'energy_consumption': 49.0,  # MJ per kg
                'recyclability': 0.75,  # 0-1 scale
                'biodegradability': 0.95,  # 0-1 scale
                'toxicity': 0.15,  # 0-1 scale
                'resource_depletion': 0.4  # 0-1 scale
            },
            'polyester': {
                'carbon_footprint': 6.4,  # kg CO2e per kg
                'water_usage': 125.0,  # liters per kg
                'energy_consumption': 125.0,  # MJ per kg
                'recyclability': 0.7,  # 0-1 scale
                'biodegradability': 0.05,  # 0-1 scale
                'toxicity': 0.3,  # 0-1 scale
                'resource_depletion': 0.75  # 0-1 scale
            },
            'porcelain': {
                'carbon_footprint': 1.2,  # kg CO2e per kg
                'water_usage': 30.0,  # liters per kg
                'energy_consumption': 27.0,  # MJ per kg
                'recyclability': 0.4,  # 0-1 scale
                'biodegradability': 0.0,  # 0-1 scale
                'toxicity': 0.1,  # 0-1 scale
                'resource_depletion': 0.35  # 0-1 scale
            },
            'carbon_fiber': {
                'carbon_footprint': 31.0,  # kg CO2e per kg
                'water_usage': 215.0,  # liters per kg
                'energy_consumption': 286.0,  # MJ per kg
                'recyclability': 0.3,  # 0-1 scale
                'biodegradability': 0.0,  # 0-1 scale
                'toxicity': 0.35,  # 0-1 scale
                'resource_depletion': 0.8  # 0-1 scale
            },
            'soda_lime_glass': {
                'carbon_footprint': 0.85,  # kg CO2e per kg
                'water_usage': 16.0,  # liters per kg
                'energy_consumption': 15.0,  # MJ per kg
                'recyclability': 0.9,  # 0-1 scale
                'biodegradability': 0.0,  # 0-1 scale
                'toxicity': 0.05,  # 0-1 scale
                'resource_depletion': 0.25  # 0-1 scale
            },
            'cork': {
                'carbon_footprint': 0.2,  # kg CO2e per kg
                'water_usage': 5.0,  # liters per kg
                'energy_consumption': 4.0,  # MJ per kg
                'recyclability': 0.9,  # 0-1 scale
                'biodegradability': 0.98,  # 0-1 scale
                'toxicity': 0.01,  # 0-1 scale
                'resource_depletion': 0.05  # 0-1 scale
            },
            'silicone': {
                'carbon_footprint': 3.5,  # kg CO2e per kg
                'water_usage': 85.0,  # liters per kg
                'energy_consumption': 65.0,  # MJ per kg
                'recyclability': 0.3,  # 0-1 scale
                'biodegradability': 0.02,  # 0-1 scale
                'toxicity': 0.2,  # 0-1 scale
                'resource_depletion': 0.6  # 0-1 scale
            }
        }
        
        # Initialize manufacturing processes environmental impact data
        self.manufacturing_impact = {
            'injection_molding': {
                'carbon_footprint': 1.1,  # kg CO2e per kg of product
                'water_usage': 20.0,  # liters per kg of product
                'energy_consumption': 18.0,  # MJ per kg of product
                'waste_generation': 0.15,  # kg waste per kg of product
                'process_efficiency': 0.85,  # 0-1 scale
                'automation_potential': 0.9  # 0-1 scale
            },
            'extrusion': {
                'carbon_footprint': 0.8,  # kg CO2e per kg of product
                'water_usage': 15.0,  # liters per kg of product
                'energy_consumption': 14.0,  # MJ per kg of product
                'waste_generation': 0.1,  # kg waste per kg of product
                'process_efficiency': 0.9,  # 0-1 scale
                'automation_potential': 0.85  # 0-1 scale
            },
            'cnc_machining': {
                'carbon_footprint': 1.5,  # kg CO2e per kg of product
                'water_usage': 25.0,  # liters per kg of product
                'energy_consumption': 30.0,  # MJ per kg of product
                'waste_generation': 0.4,  # kg waste per kg of product
                'process_efficiency': 0.7,  # 0-1 scale
                'automation_potential': 0.95  # 0-1 scale
            },
            '3d_printing': {
                'carbon_footprint': 2.0,  # kg CO2e per kg of product
                'water_usage': 5.0,  # liters per kg of product
                'energy_consumption': 50.0,  # MJ per kg of product
                'waste_generation': 0.2,  # kg waste per kg of product
                'process_efficiency': 0.75,  # 0-1 scale
                'automation_potential': 0.9  # 0-1 scale
            },
            'casting': {
                'carbon_footprint': 2.5,  # kg CO2e per kg of product
                'water_usage': 40.0,  # liters per kg of product
                'energy_consumption': 45.0,  # MJ per kg of product
                'waste_generation': 0.25,  # kg waste per kg of product
                'process_efficiency': 0.8,  # 0-1 scale
                'automation_potential': 0.7  # 0-1 scale
            },
            'forging': {
                'carbon_footprint': 1.8,  # kg CO2e per kg of product
                'water_usage': 30.0,  # liters per kg of product
                'energy_consumption': 40.0,  # MJ per kg of product
                'waste_generation': 0.15,  # kg waste per kg of product
                'process_efficiency': 0.85,  # 0-1 scale
                'automation_potential': 0.75  # 0-1 scale
            },
            'welding': {
                'carbon_footprint': 0.9,  # kg CO2e per kg of product
                'water_usage': 5.0,  # liters per kg of product
                'energy_consumption': 25.0,  # MJ per kg of product
                'waste_generation': 0.05,  # kg waste per kg of product
                'process_efficiency': 0.8,  # 0-1 scale
                'automation_potential': 0.8  # 0-1 scale
            },
            'woodworking': {
                'carbon_footprint': 0.5,  # kg CO2e per kg of product
                'water_usage': 10.0,  # liters per kg of product
                'energy_consumption': 12.0,  # MJ per kg of product
                'waste_generation': 0.3,  # kg waste per kg of product
                'process_efficiency': 0.75,  # 0-1 scale
                'automation_potential': 0.7  # 0-1 scale
            },
            'sewing': {
                'carbon_footprint': 0.3,  # kg CO2e per kg of product
                'water_usage': 5.0,  # liters per kg of product
                'energy_consumption': 8.0,  # MJ per kg of product
                'waste_generation': 0.15,  # kg waste per kg of product
                'process_efficiency': 0.8,  # 0-1 scale
                'automation_potential': 0.6  # 0-1 scale
            },
            'assembly': {
                'carbon_footprint': 0.2,  # kg CO2e per kg of product
                'water_usage': 3.0,  # liters per kg of product
                'energy_consumption': 5.0,  # MJ per kg of product
                'waste_generation': 0.05,  # kg waste per kg of product
                'process_efficiency': 0.9,  # 0-1 scale
                'automation_potential': 0.85  # 0-1 scale
            }
        }
        
        # Initialize lifecycle factors
        self.lifecycle_factors = {
            'transportation': {
                'local': {
                    'carbon_footprint': 0.1,  # kg CO2e per kg-km
                    'energy_consumption': 1.0  # MJ per kg-km
                },
                'regional': {
                    'carbon_footprint': 0.05,  # kg CO2e per kg-km
                    'energy_consumption': 0.8  # MJ per kg-km
                },
                'international': {
                    'carbon_footprint': 0.02,  # kg CO2e per kg-km
                    'energy_consumption': 0.5  # MJ per kg-km
                }
            },
            'packaging': {
                'minimal': {
                    'material_usage': 0.05,  # kg packaging per kg product
                    'recyclability': 0.9  # 0-1 scale
                },
                'standard': {
                    'material_usage': 0.15,  # kg packaging per kg product
                    'recyclability': 0.7  # 0-1 scale
                },
                'premium': {
                    'material_usage': 0.3,  # kg packaging per kg product
                    'recyclability': 0.5  # 0-1 scale
                }
            },
            'use_phase': {
                'energy_intensive': {
                    'lifetime_energy': 1000.0,  # MJ over product lifetime
                    'lifetime_emissions': 50.0  # kg CO2e over product lifetime
                },
                'moderate_energy': {
                    'lifetime_energy': 100.0,  # MJ over product lifetime
                    'lifetime_emissions': 5.0  # kg CO2e over product lifetime
                },
                'low_energy': {
                    'lifetime_energy': 10.0,  # MJ over product lifetime
                    'lifetime_emissions': 0.5  # kg CO2e over product lifetime
                },
                'passive': {
                    'lifetime_energy': 0.0,  # MJ over product lifetime
                    'lifetime_emissions': 0.0  # kg CO2e over product lifetime
                }
            },
            'end_of_life': {
                'landfill': {
                    'recovery_rate': 0.0,  # 0-1 scale
                    'emissions': 0.5  # kg CO2e per kg of product
                },
                'incineration': {
                    'recovery_rate': 0.3,  # 0-1 scale (energy recovery)
                    'emissions': 2.0  # kg CO2e per kg of product
                },
                'recycling': {
                    'recovery_rate': 0.8,  # 0-1 scale
                    'emissions': 0.2  # kg CO2e per kg of product
                },
                'composting': {
                    'recovery_rate': 0.9,  # 0-1 scale
                    'emissions': 0.1  # kg CO2e per kg of product
                },
                'reuse': {
                    'recovery_rate': 0.95,  # 0-1 scale
                    'emissions': 0.05  # kg CO2e per kg of product
                }
            }
        }
        
        # Initialize sustainability data
        self.sustainability_data = {
            'materials_impact': self.materials_impact,
            'manufacturing_impact': self.manufacturing_impact,
            'lifecycle_factors': self.lifecycle_factors,
            'sustainability_principles': [
                {
                    'name': 'Material Efficiency',
                    'description': 'Use materials efficiently to minimize waste and resource consumption',
                    'strategies': [
                        'Lightweight design',
                        'Material optimization',
                        'Waste reduction',
                        'Recycled content'
                    ]
                },
                {
                    'name': 'Energy Efficiency',
                    'description': 'Minimize energy consumption throughout the product lifecycle',
                    'strategies': [
                        'Low-energy manufacturing',
                        'Energy-efficient use phase',
                        'Reduced transportation energy',
                        'Renewable energy sources'
                    ]
                },
                {
                    'name': 'Water Conservation',
                    'description': 'Reduce water usage and pollution throughout the product lifecycle',
                    'strategies': [
                        'Water-efficient materials',
                        'Water-efficient manufacturing',
                        'Water-efficient use phase',
                        'Water pollution prevention'
                    ]
                },
                {
                    'name': 'Toxicity Reduction',
                    'description': 'Minimize the use of toxic substances and their release into the environment',
                    'strategies': [
                        'Non-toxic materials',
                        'Clean manufacturing processes',
                        'Safe use phase',
                        'Safe disposal'
                    ]
                },
                {
                    'name': 'Durability and Longevity',
                    'description': 'Design products to last longer and maintain their value over time',
                    'strategies': [
                        'Robust design',
                        'Quality materials',
                        'Repairability',
                        'Upgradability'
                    ]
                },
                {
                    'name': 'Circular Economy',
                    'description': 'Design for circularity to keep materials and products in use',
                    'strategies': [
                        'Design for disassembly',
                        'Recyclability',
                        'Reusability',
                        'Biodegradability'
                    ]
                },
                {
                    'name': 'Renewable Resources',
                    'description': 'Prioritize renewable and regenerative resources',
                    'strategies': [
                        'Bio-based materials',
                        'Rapidly renewable materials',
                        'Sustainable harvesting',
                        'Regenerative practices'
                    ]
                }
            ]
        }
        
        logger.info("Initialized default sustainability database")
    
    def save_database(self, output_path=None):
        """
        Save the sustainability database to a file.
        
        Args:
            output_path (str, optional): Path to save the database file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            path = output_path or self.database_path
            if not path:
                logger.warning("No output path specified for saving database")
                return False
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Save database to file
            with open(path, 'w') as f:
                json.dump({
                    'sustainability_data': self.sustainability_data,
                    'materials_impact': self.materials_impact,
                    'manufacturing_impact': self.manufacturing_impact,
                    'lifecycle_factors': self.lifecycle_factors,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"Saved sustainability database to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving sustainability database: {str(e)}")
            return False
    
    def analyze_material_sustainability(self, material_id):
        """
        Analyze the sustainability of a specific material.
        
        Args:
            material_id (str): Material identifier
            
        Returns:
            dict: Sustainability analysis
        """
        if material_id not in self.materials_impact:
            return {
                'material': material_id,
                'sustainability_score': 0,
                'error': 'Material not found in database'
            }
        
        # Get material impact data
        impact_data = self.materials_impact[material_id]
        
        # Calculate sustainability score (0-100)
        # Lower values for carbon footprint, water usage, energy consumption, toxicity, resource depletion are better
        # Higher values for recyclability, biodegradability are better
        
        # Normalize values to 0-1 scale (where 1 is most sustainable)
        normalized_carbon = max(0, 1 - (impact_data['carbon_footprint'] / 30))  # Assuming 30 kg CO2e/kg is max
        normalized_water = max(0, 1 - (impact_data['water_usage'] / 10000))  # Assuming 10000 L/kg is max
        normalized_energy = max(0, 1 - (impact_data['energy_consumption'] / 300))  # Assuming 300 MJ/kg is max
        
        # Direct values (already 0-1)
        recyclability = impact_data['recyclability']
        biodegradability = impact_data['biodegradability']
        toxicity = 1 - impact_data['toxicity']  # Invert so higher is better
        resource_depletion = 1 - impact_data['resource_depletion']  # Invert so higher is better
        
        # Calculate weighted score
        weights = {
            'carbon': 0.2,
            'water': 0.15,
            'energy': 0.15,
            'recyclability': 0.15,
            'biodegradability': 0.1,
            'toxicity': 0.1,
            'resource_depletion': 0.15
        }
        
        sustainability_score = (
            weights['carbon'] * normalized_carbon +
            weights['water'] * normalized_water +
            weights['energy'] * normalized_energy +
            weights['recyclability'] * recyclability +
            weights['biodegradability'] * biodegradability +
            weights['toxicity'] * toxicity +
            weights['resource_depletion'] * resource_depletion
        ) * 100  # Scale to 0-100
        
        # Determine sustainability level
        if sustainability_score >= 80:
            sustainability_level = 'Excellent'
        elif sustainability_score >= 60:
            sustainability_level = 'Good'
        elif sustainability_score >= 40:
            sustainability_level = 'Moderate'
        elif sustainability_score >= 20:
            sustainability_level = 'Poor'
        else:
            sustainability_level = 'Very Poor'
        
        # Generate strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if normalized_carbon >= 0.7:
            strengths.append('Low carbon footprint')
        elif normalized_carbon <= 0.3:
            weaknesses.append('High carbon footprint')
        
        if normalized_water >= 0.7:
            strengths.append('Low water usage')
        elif normalized_water <= 0.3:
            weaknesses.append('High water usage')
        
        if normalized_energy >= 0.7:
            strengths.append('Low energy consumption')
        elif normalized_energy <= 0.3:
            weaknesses.append('High energy consumption')
        
        if recyclability >= 0.7:
            strengths.append('Highly recyclable')
        elif recyclability <= 0.3:
            weaknesses.append('Poor recyclability')
        
        if biodegradability >= 0.7:
            strengths.append('Biodegradable')
        elif biodegradability <= 0.3:
            weaknesses.append('Non-biodegradable')
        
        if toxicity >= 0.7:
            strengths.append('Low toxicity')
        elif toxicity <= 0.3:
            weaknesses.append('High toxicity')
        
        if resource_depletion >= 0.7:
            strengths.append('Low resource depletion')
        elif resource_depletion <= 0.3:
            weaknesses.append('High resource depletion')
        
        # Create analysis result
        analysis = {
            'material': material_id,
            'sustainability_score': round(sustainability_score, 1),
            'sustainability_level': sustainability_level,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'impact_data': impact_data
        }
        
        return analysis
    
    def analyze_manufacturing_sustainability(self, process_id):
        """
        Analyze the sustainability of a specific manufacturing process.
        
        Args:
            process_id (str): Manufacturing process identifier
            
        Returns:
            dict: Sustainability analysis
        """
        if process_id not in self.manufacturing_impact:
            return {
                'process': process_id,
                'sustainability_score': 0,
                'error': 'Manufacturing process not found in database'
            }
        
        # Get process impact data
        impact_data = self.manufacturing_impact[process_id]
        
        # Calculate sustainability score (0-100)
        # Lower values for carbon footprint, water usage, energy consumption, waste generation are better
        # Higher values for process efficiency, automation potential are better
        
        # Normalize values to 0-1 scale (where 1 is most sustainable)
        normalized_carbon = max(0, 1 - (impact_data['carbon_footprint'] / 3))  # Assuming 3 kg CO2e/kg is max
        normalized_water = max(0, 1 - (impact_data['water_usage'] / 50))  # Assuming 50 L/kg is max
        normalized_energy = max(0, 1 - (impact_data['energy_consumption'] / 50))  # Assuming 50 MJ/kg is max
        normalized_waste = max(0, 1 - (impact_data['waste_generation'] / 0.5))  # Assuming 0.5 kg waste/kg is max
        
        # Direct values (already 0-1)
        efficiency = impact_data['process_efficiency']
        automation = impact_data['automation_potential']
        
        # Calculate weighted score
        weights = {
            'carbon': 0.2,
            'water': 0.15,
            'energy': 0.2,
            'waste': 0.2,
            'efficiency': 0.15,
            'automation': 0.1
        }
        
        sustainability_score = (
            weights['carbon'] * normalized_carbon +
            weights['water'] * normalized_water +
            weights['energy'] * normalized_energy +
            weights['waste'] * normalized_waste +
            weights['efficiency'] * efficiency +
            weights['automation'] * automation
        ) * 100  # Scale to 0-100
        
        # Determine sustainability level
        if sustainability_score >= 80:
            sustainability_level = 'Excellent'
        elif sustainability_score >= 60:
            sustainability_level = 'Good'
        elif sustainability_score >= 40:
            sustainability_level = 'Moderate'
        elif sustainability_score >= 20:
            sustainability_level = 'Poor'
        else:
            sustainability_level = 'Very Poor'
        
        # Generate strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if normalized_carbon >= 0.7:
            strengths.append('Low carbon footprint')
        elif normalized_carbon <= 0.3:
            weaknesses.append('High carbon footprint')
        
        if normalized_water >= 0.7:
            strengths.append('Low water usage')
        elif normalized_water <= 0.3:
            weaknesses.append('High water usage')
        
        if normalized_energy >= 0.7:
            strengths.append('Low energy consumption')
        elif normalized_energy <= 0.3:
            weaknesses.append('High energy consumption')
        
        if normalized_waste >= 0.7:
            strengths.append('Low waste generation')
        elif normalized_waste <= 0.3:
            weaknesses.append('High waste generation')
        
        if efficiency >= 0.7:
            strengths.append('High process efficiency')
        elif efficiency <= 0.3:
            weaknesses.append('Low process efficiency')
        
        if automation >= 0.7:
            strengths.append('High automation potential')
        elif automation <= 0.3:
            weaknesses.append('Low automation potential')
        
        # Create analysis result
        analysis = {
            'process': process_id,
            'sustainability_score': round(sustainability_score, 1),
            'sustainability_level': sustainability_level,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'impact_data': impact_data
        }
        
        return analysis
    
    def analyze_product_sustainability(self, product_data):
        """
        Analyze the sustainability of a product design.
        
        Args:
            product_data (dict): Product design data including materials, manufacturing processes, etc.
            
        Returns:
            dict: Sustainability analysis
        """
        try:
            # Extract product components
            components = product_data.get('components', [])
            if not components:
                return {
                    'product': product_data.get('name', 'Unknown'),
                    'sustainability_score': 0,
                    'error': 'No components found in product data'
                }
            
            # Analyze each component
            component_analyses = []
            total_weight = 0
            
            for component in components:
                material_id = component.get('material')
                process_id = component.get('manufacturing_process')
                weight = component.get('weight', 1.0)  # kg
                
                # Analyze material
                material_analysis = self.analyze_material_sustainability(material_id) if material_id else None
                
                # Analyze manufacturing process
                process_analysis = self.analyze_manufacturing_sustainability(process_id) if process_id else None
                
                # Calculate component sustainability score
                component_score = 0
                if material_analysis and 'sustainability_score' in material_analysis:
                    component_score += 0.7 * material_analysis['sustainability_score']
                if process_analysis and 'sustainability_score' in process_analysis:
                    component_score += 0.3 * process_analysis['sustainability_score']
                
                # Add component analysis
                component_analyses.append({
                    'name': component.get('name', 'Component'),
                    'material': material_id,
                    'process': process_id,
                    'weight': weight,
                    'sustainability_score': round(component_score, 1),
                    'material_analysis': material_analysis,
                    'process_analysis': process_analysis
                })
                
                total_weight += weight
            
            # Calculate overall product sustainability score
            if total_weight > 0:
                product_score = sum(c['sustainability_score'] * c['weight'] for c in component_analyses) / total_weight
            else:
                product_score = sum(c['sustainability_score'] for c in component_analyses) / len(component_analyses)
            
            # Analyze lifecycle factors
            lifecycle_score = self._analyze_lifecycle_factors(product_data)
            
            # Combine scores (70% components, 30% lifecycle)
            overall_score = 0.7 * product_score + 0.3 * lifecycle_score
            
            # Determine sustainability level
            if overall_score >= 80:
                sustainability_level = 'Excellent'
            elif overall_score >= 60:
                sustainability_level = 'Good'
            elif overall_score >= 40:
                sustainability_level = 'Moderate'
            elif overall_score >= 20:
                sustainability_level = 'Poor'
            else:
                sustainability_level = 'Very Poor'
            
            # Generate improvement recommendations
            recommendations = self._generate_sustainability_recommendations(component_analyses, product_data)
            
            # Create analysis result
            analysis = {
                'product': product_data.get('name', 'Unknown'),
                'sustainability_score': round(overall_score, 1),
                'sustainability_level': sustainability_level,
                'component_analyses': component_analyses,
                'lifecycle_analysis': {
                    'score': round(lifecycle_score, 1)
                },
                'recommendations': recommendations
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing product sustainability: {str(e)}")
            return {
                'product': product_data.get('name', 'Unknown'),
                'sustainability_score': 0,
                'error': str(e)
            }
    
    def _analyze_lifecycle_factors(self, product_data):
        """
        Analyze lifecycle factors for sustainability.
        
        Args:
            product_data (dict): Product design data
            
        Returns:
            float: Lifecycle sustainability score (0-100)
        """
        # Extract lifecycle data
        lifecycle = product_data.get('lifecycle', {})
        
        # Default values if not specified
        transportation_type = lifecycle.get('transportation', 'regional')
        packaging_type = lifecycle.get('packaging', 'standard')
        use_phase_type = lifecycle.get('use_phase', 'moderate_energy')
        end_of_life_type = lifecycle.get('end_of_life', 'recycling')
        
        # Get lifecycle factors
        transportation_factors = self.lifecycle_factors['transportation'].get(transportation_type, 
                                                                             self.lifecycle_factors['transportation']['regional'])
        packaging_factors = self.lifecycle_factors['packaging'].get(packaging_type, 
                                                                   self.lifecycle_factors['packaging']['standard'])
        use_phase_factors = self.lifecycle_factors['use_phase'].get(use_phase_type, 
                                                                   self.lifecycle_factors['use_phase']['moderate_energy'])
        end_of_life_factors = self.lifecycle_factors['end_of_life'].get(end_of_life_type, 
                                                                       self.lifecycle_factors['end_of_life']['recycling'])
        
        # Calculate transportation score (0-100)
        # Lower values for carbon footprint and energy consumption are better
        transportation_carbon_score = max(0, 100 - (transportation_factors['carbon_footprint'] * 1000))
        transportation_energy_score = max(0, 100 - (transportation_factors['energy_consumption'] * 100))
        transportation_score = 0.5 * transportation_carbon_score + 0.5 * transportation_energy_score
        
        # Calculate packaging score (0-100)
        # Lower values for material usage are better, higher values for recyclability are better
        packaging_material_score = max(0, 100 - (packaging_factors['material_usage'] * 300))
        packaging_recyclability_score = packaging_factors['recyclability'] * 100
        packaging_score = 0.5 * packaging_material_score + 0.5 * packaging_recyclability_score
        
        # Calculate use phase score (0-100)
        # Lower values for lifetime energy and emissions are better
        use_energy_score = max(0, 100 - (use_phase_factors['lifetime_energy'] / 10))
        use_emissions_score = max(0, 100 - (use_phase_factors['lifetime_emissions'] * 2))
        use_phase_score = 0.5 * use_energy_score + 0.5 * use_emissions_score
        
        # Calculate end of life score (0-100)
        # Higher values for recovery rate are better, lower values for emissions are better
        eol_recovery_score = end_of_life_factors['recovery_rate'] * 100
        eol_emissions_score = max(0, 100 - (end_of_life_factors['emissions'] * 50))
        end_of_life_score = 0.6 * eol_recovery_score + 0.4 * eol_emissions_score
        
        # Calculate overall lifecycle score with weights
        weights = {
            'transportation': 0.2,
            'packaging': 0.1,
            'use_phase': 0.4,
            'end_of_life': 0.3
        }
        
        lifecycle_score = (
            weights['transportation'] * transportation_score +
            weights['packaging'] * packaging_score +
            weights['use_phase'] * use_phase_score +
            weights['end_of_life'] * end_of_life_score
        )
        
        return lifecycle_score
    
    def _generate_sustainability_recommendations(self, component_analyses, product_data):
        """
        Generate sustainability improvement recommendations.
        
        Args:
            component_analyses (list): Component sustainability analyses
            product_data (dict): Product design data
            
        Returns:
            list: Sustainability recommendations
        """
        recommendations = []
        
        # Identify components with low sustainability scores
        low_sustainability_components = [c for c in component_analyses if c['sustainability_score'] < 50]
        
        # Generate material recommendations
        for component in low_sustainability_components:
            material_analysis = component.get('material_analysis')
            if material_analysis and 'weaknesses' in material_analysis:
                material_id = component.get('material')
                
                # Recommend alternative materials based on weaknesses
                if 'High carbon footprint' in material_analysis['weaknesses']:
                    alternatives = self._find_alternative_materials(material_id, 'carbon_footprint', 'low')
                    if alternatives:
                        recommendations.append({
                            'type': 'material_substitution',
                            'component': component.get('name'),
                            'current_material': material_id,
                            'suggested_materials': alternatives,
                            'reason': 'Reduce carbon footprint',
                            'potential_improvement': 'Medium to High'
                        })
                
                if 'High water usage' in material_analysis['weaknesses']:
                    alternatives = self._find_alternative_materials(material_id, 'water_usage', 'low')
                    if alternatives:
                        recommendations.append({
                            'type': 'material_substitution',
                            'component': component.get('name'),
                            'current_material': material_id,
                            'suggested_materials': alternatives,
                            'reason': 'Reduce water usage',
                            'potential_improvement': 'Medium to High'
                        })
                
                if 'Poor recyclability' in material_analysis['weaknesses']:
                    alternatives = self._find_alternative_materials(material_id, 'recyclability', 'high')
                    if alternatives:
                        recommendations.append({
                            'type': 'material_substitution',
                            'component': component.get('name'),
                            'current_material': material_id,
                            'suggested_materials': alternatives,
                            'reason': 'Improve recyclability',
                            'potential_improvement': 'Medium to High'
                        })
        
        # Generate manufacturing process recommendations
        for component in low_sustainability_components:
            process_analysis = component.get('process_analysis')
            if process_analysis and 'weaknesses' in process_analysis:
                process_id = component.get('process')
                
                # Recommend alternative processes based on weaknesses
                if 'High energy consumption' in process_analysis['weaknesses']:
                    alternatives = self._find_alternative_processes(process_id, 'energy_consumption', 'low')
                    if alternatives:
                        recommendations.append({
                            'type': 'process_substitution',
                            'component': component.get('name'),
                            'current_process': process_id,
                            'suggested_processes': alternatives,
                            'reason': 'Reduce energy consumption',
                            'potential_improvement': 'Medium'
                        })
                
                if 'High waste generation' in process_analysis['weaknesses']:
                    alternatives = self._find_alternative_processes(process_id, 'waste_generation', 'low')
                    if alternatives:
                        recommendations.append({
                            'type': 'process_substitution',
                            'component': component.get('name'),
                            'current_process': process_id,
                            'suggested_processes': alternatives,
                            'reason': 'Reduce waste generation',
                            'potential_improvement': 'Medium'
                        })
        
        # Generate lifecycle recommendations
        lifecycle = product_data.get('lifecycle', {})
        
        # Transportation recommendations
        transportation_type = lifecycle.get('transportation', 'regional')
        if transportation_type == 'international':
            recommendations.append({
                'type': 'lifecycle_improvement',
                'category': 'transportation',
                'current': transportation_type,
                'suggestion': 'Consider local or regional sourcing to reduce transportation emissions',
                'reason': 'Reduce carbon footprint from long-distance transportation',
                'potential_improvement': 'Medium'
            })
        
        # Packaging recommendations
        packaging_type = lifecycle.get('packaging', 'standard')
        if packaging_type == 'premium':
            recommendations.append({
                'type': 'lifecycle_improvement',
                'category': 'packaging',
                'current': packaging_type,
                'suggestion': 'Consider minimal or standard packaging with higher recyclability',
                'reason': 'Reduce packaging material usage and improve recyclability',
                'potential_improvement': 'Low to Medium'
            })
        
        # Use phase recommendations
        use_phase_type = lifecycle.get('use_phase', 'moderate_energy')
        if use_phase_type == 'energy_intensive':
            recommendations.append({
                'type': 'lifecycle_improvement',
                'category': 'use_phase',
                'current': use_phase_type,
                'suggestion': 'Improve energy efficiency during use phase',
                'reason': 'Reduce lifetime energy consumption and emissions',
                'potential_improvement': 'High'
            })
        
        # End of life recommendations
        end_of_life_type = lifecycle.get('end_of_life', 'recycling')
        if end_of_life_type in ['landfill', 'incineration']:
            recommendations.append({
                'type': 'lifecycle_improvement',
                'category': 'end_of_life',
                'current': end_of_life_type,
                'suggestion': 'Design for recyclability, reuse, or composting',
                'reason': 'Improve end-of-life recovery and reduce disposal emissions',
                'potential_improvement': 'High'
            })
        
        # Design recommendations
        design_recommendations = [
            {
                'type': 'design_principle',
                'principle': 'Material Reduction',
                'suggestion': 'Optimize design to use less material while maintaining performance',
                'reason': 'Reduce resource consumption and environmental impact',
                'potential_improvement': 'Medium'
            },
            {
                'type': 'design_principle',
                'principle': 'Design for Disassembly',
                'suggestion': 'Design product for easy disassembly at end of life',
                'reason': 'Facilitate repair, recycling, and component reuse',
                'potential_improvement': 'Medium to High'
            },
            {
                'type': 'design_principle',
                'principle': 'Mono-material Design',
                'suggestion': 'Where possible, use single materials or compatible material combinations',
                'reason': 'Simplify recycling and improve material recovery',
                'potential_improvement': 'Medium'
            }
        ]
        
        # Add design recommendations (limit to 2 to avoid overwhelming)
        recommendations.extend(design_recommendations[:2])
        
        return recommendations
    
    def _find_alternative_materials(self, material_id, property_name, preference):
        """
        Find alternative materials with better sustainability properties.
        
        Args:
            material_id (str): Current material identifier
            property_name (str): Property to improve
            preference (str): 'high' or 'low' indicating whether higher or lower values are better
            
        Returns:
            list: Alternative materials
        """
        if material_id not in self.materials_impact:
            return []
        
        current_value = self.materials_impact[material_id].get(property_name, 0)
        alternatives = []
        
        for alt_id, alt_data in self.materials_impact.items():
            if alt_id == material_id:
                continue
            
            alt_value = alt_data.get(property_name, 0)
            
            # Check if alternative is better
            is_better = False
            if preference == 'high':
                is_better = alt_value > current_value
            elif preference == 'low':
                is_better = alt_value < current_value
            
            if is_better:
                improvement = abs(alt_value - current_value) / max(current_value, 0.001)
                if improvement > 0.2:  # Only suggest if improvement is significant
                    alternatives.append({
                        'id': alt_id,
                        'improvement': round(improvement * 100, 1)
                    })
        
        # Sort by improvement (descending) and limit to top 3
        alternatives.sort(key=lambda x: x['improvement'], reverse=True)
        return alternatives[:3]
    
    def _find_alternative_processes(self, process_id, property_name, preference):
        """
        Find alternative manufacturing processes with better sustainability properties.
        
        Args:
            process_id (str): Current process identifier
            property_name (str): Property to improve
            preference (str): 'high' or 'low' indicating whether higher or lower values are better
            
        Returns:
            list: Alternative processes
        """
        if process_id not in self.manufacturing_impact:
            return []
        
        current_value = self.manufacturing_impact[process_id].get(property_name, 0)
        alternatives = []
        
        for alt_id, alt_data in self.manufacturing_impact.items():
            if alt_id == process_id:
                continue
            
            alt_value = alt_data.get(property_name, 0)
            
            # Check if alternative is better
            is_better = False
            if preference == 'high':
                is_better = alt_value > current_value
            elif preference == 'low':
                is_better = alt_value < current_value
            
            if is_better:
                improvement = abs(alt_value - current_value) / max(current_value, 0.001)
                if improvement > 0.2:  # Only suggest if improvement is significant
                    alternatives.append({
                        'id': alt_id,
                        'improvement': round(improvement * 100, 1)
                    })
        
        # Sort by improvement (descending) and limit to top 3
        alternatives.sort(key=lambda x: x['improvement'], reverse=True)
        return alternatives[:3]
    
    def get_sustainability_principles(self):
        """
        Get sustainability design principles.
        
        Returns:
            list: Sustainability principles
        """
        return self.sustainability_data.get('sustainability_principles', [])
    
    def get_eco_design_strategies(self, industry=None):
        """
        Get eco-design strategies, optionally filtered by industry.
        
        Args:
            industry (str, optional): Industry to filter strategies
            
        Returns:
            list: Eco-design strategies
        """
        # Base strategies applicable to all industries
        base_strategies = [
            {
                'name': 'Material Selection',
                'description': 'Choose materials with lower environmental impact',
                'tactics': [
                    'Use recycled or recyclable materials',
                    'Use renewable and bio-based materials',
                    'Avoid toxic or hazardous materials',
                    'Select materials with lower carbon footprint'
                ]
            },
            {
                'name': 'Material Efficiency',
                'description': 'Optimize material usage to reduce waste',
                'tactics': [
                    'Lightweight design',
                    'Structural optimization',
                    'Minimize material variety',
                    'Reduce manufacturing waste'
                ]
            },
            {
                'name': 'Energy Efficiency',
                'description': 'Reduce energy consumption throughout the product lifecycle',
                'tactics': [
                    'Design for low-energy manufacturing',
                    'Improve energy efficiency during use',
                    'Reduce energy for transportation',
                    'Use renewable energy sources'
                ]
            },
            {
                'name': 'Longevity and Durability',
                'description': 'Extend product lifespan to reduce replacement frequency',
                'tactics': [
                    'Design for durability',
                    'Enable easy repair and maintenance',
                    'Allow for upgrades and adaptability',
                    'Create timeless aesthetics'
                ]
            },
            {
                'name': 'End-of-Life Optimization',
                'description': 'Improve product recovery at end of life',
                'tactics': [
                    'Design for disassembly',
                    'Design for recyclability',
                    'Enable component reuse',
                    'Consider biodegradability for appropriate products'
                ]
            }
        ]
        
        # Industry-specific strategies
        industry_strategies = {
            'furniture': [
                {
                    'name': 'Modular Design',
                    'description': 'Create furniture with interchangeable components',
                    'tactics': [
                        'Standardized connection systems',
                        'Replaceable parts',
                        'Adaptable configurations',
                        'Multi-functional elements'
                    ]
                },
                {
                    'name': 'Local Sourcing',
                    'description': 'Source materials and manufacturing locally',
                    'tactics': [
                        'Use locally available materials',
                        'Partner with local manufacturers',
                        'Reduce transportation emissions',
                        'Support local economies'
                    ]
                }
            ],
            'electronics': [
                {
                    'name': 'Energy Optimization',
                    'description': 'Minimize energy consumption during use',
                    'tactics': [
                        'Efficient power management',
                        'Low-power components',
                        'Energy-saving modes',
                        'Renewable energy compatibility'
                    ]
                },
                {
                    'name': 'Hazardous Substance Reduction',
                    'description': 'Eliminate or reduce hazardous materials',
                    'tactics': [
                        'RoHS compliance',
                        'Lead-free solder',
                        'Halogen-free flame retardants',
                        'Non-toxic batteries'
                    ]
                }
            ],
            'packaging': [
                {
                    'name': 'Material Reduction',
                    'description': 'Minimize packaging material while maintaining protection',
                    'tactics': [
                        'Structural optimization',
                        'Eliminate unnecessary layers',
                        'Right-sizing packages',
                        'Concentrated products'
                    ]
                },
                {
                    'name': 'Circular Packaging',
                    'description': 'Design packaging for circular economy',
                    'tactics': [
                        'Reusable packaging systems',
                        'Mono-material designs',
                        'Easily recyclable materials',
                        'Compostable alternatives'
                    ]
                }
            ],
            'fashion': [
                {
                    'name': 'Sustainable Textiles',
                    'description': 'Choose textiles with lower environmental impact',
                    'tactics': [
                        'Organic and natural fibers',
                        'Recycled textiles',
                        'Low-impact dyes and finishes',
                        'Water-efficient processing'
                    ]
                },
                {
                    'name': 'Timeless Design',
                    'description': 'Create designs that transcend seasonal trends',
                    'tactics': [
                        'Classic silhouettes',
                        'Versatile styling',
                        'Quality construction',
                        'Adaptable features'
                    ]
                }
            ]
        }
        
        # Return strategies based on industry filter
        if industry and industry in industry_strategies:
            return base_strategies + industry_strategies[industry]
        elif industry:
            return base_strategies
        else:
            # Return all strategies
            all_strategies = base_strategies.copy()
            for strategies in industry_strategies.values():
                all_strategies.extend(strategies)
            return all_strategies


if __name__ == "__main__":
    # Example usage
    analyzer = SustainabilityAnalyzer()
    
    # Analyze material sustainability
    bamboo_analysis = analyzer.analyze_material_sustainability('bamboo')
    print(f"Bamboo sustainability score: {bamboo_analysis['sustainability_score']}")
    print(f"Strengths: {bamboo_analysis['strengths']}")
    print(f"Weaknesses: {bamboo_analysis['weaknesses']}")
    
    # Analyze manufacturing process sustainability
    process_analysis = analyzer.analyze_manufacturing_sustainability('injection_molding')
    print(f"Injection molding sustainability score: {process_analysis['sustainability_score']}")
    
    # Get eco-design strategies
    strategies = analyzer.get_eco_design_strategies('furniture')
    print(f"Found {len(strategies)} eco-design strategies for furniture")
