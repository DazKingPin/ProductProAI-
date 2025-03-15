import logging
import json
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MaterialDatabase:
    """
    Class for managing a comprehensive database of materials and their properties.
    Provides information about different materials across various industries.
    """
    
    def __init__(self, database_path=None):
        """
        Initialize the MaterialDatabase.
        
        Args:
            database_path (str, optional): Path to the material database file
        """
        logger.info("Initializing MaterialDatabase")
        self.database_path = database_path
        self.materials = {}
        self.categories = {}
        self._load_materials()
    
    def _load_materials(self):
        """
        Load materials from database file or initialize with default materials.
        """
        try:
            if self.database_path and os.path.exists(self.database_path):
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    self.materials = data.get('materials', {})
                    self.categories = data.get('categories', {})
                logger.info(f"Loaded {len(self.materials)} materials from database")
            else:
                logger.info("Initializing default material database")
                self._initialize_default_materials()
        except Exception as e:
            logger.error(f"Error loading materials: {str(e)}")
            self._initialize_default_materials()
    
    def _initialize_default_materials(self):
        """
        Initialize the database with default materials and their properties.
        """
        # Define material categories
        self.categories = {
            'metals': {
                'description': 'Metallic materials with high strength and conductivity',
                'properties': ['density', 'tensile_strength', 'thermal_conductivity', 'electrical_conductivity', 'melting_point', 'recyclability']
            },
            'plastics': {
                'description': 'Synthetic or semi-synthetic materials that can be molded or extruded',
                'properties': ['density', 'tensile_strength', 'thermal_conductivity', 'melting_point', 'recyclability', 'biodegradability']
            },
            'woods': {
                'description': 'Natural materials derived from trees and plants',
                'properties': ['density', 'hardness', 'moisture_content', 'grain_pattern', 'sustainability', 'workability']
            },
            'textiles': {
                'description': 'Flexible materials made from fibers, yarns, or threads',
                'properties': ['weight', 'strength', 'elasticity', 'breathability', 'water_resistance', 'sustainability']
            },
            'ceramics': {
                'description': 'Inorganic, non-metallic solids prepared by heating and cooling',
                'properties': ['density', 'hardness', 'thermal_conductivity', 'electrical_resistivity', 'brittleness', 'heat_resistance']
            },
            'composites': {
                'description': 'Materials made from two or more constituent materials with different properties',
                'properties': ['density', 'strength_to_weight_ratio', 'stiffness', 'fatigue_resistance', 'corrosion_resistance', 'customizability']
            },
            'glass': {
                'description': 'Non-crystalline, amorphous solids that are typically transparent',
                'properties': ['density', 'refractive_index', 'transparency', 'thermal_conductivity', 'brittleness', 'recyclability']
            },
            'natural_materials': {
                'description': 'Materials derived from natural sources like plants, animals, or minerals',
                'properties': ['density', 'biodegradability', 'sustainability', 'renewability', 'processing_requirements', 'durability']
            },
            'synthetic_materials': {
                'description': 'Man-made materials created through chemical processes',
                'properties': ['density', 'durability', 'chemical_resistance', 'customizability', 'production_cost', 'environmental_impact']
            }
        }
        
        # Initialize default materials
        self.materials = {
            # Metals
            'aluminum': {
                'name': 'Aluminum',
                'category': 'metals',
                'description': 'Lightweight, corrosion-resistant metal with good thermal and electrical conductivity',
                'properties': {
                    'density': 2.7,  # g/cm³
                    'tensile_strength': 310,  # MPa
                    'thermal_conductivity': 237,  # W/(m·K)
                    'electrical_conductivity': 37.7,  # MS/m
                    'melting_point': 660,  # °C
                    'recyclability': 0.9  # 0-1 scale
                },
                'applications': ['electronics', 'packaging', 'transportation', 'construction'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'high',
                    'water_usage': 'medium'
                },
                'processing_methods': ['casting', 'extrusion', 'rolling', 'machining'],
                'finish_options': ['anodized', 'polished', 'brushed', 'painted'],
                'cost_factor': 0.6  # 0-1 scale, relative to category
            },
            'steel': {
                'name': 'Steel',
                'category': 'metals',
                'description': 'Strong, durable alloy of iron and carbon with various alloying elements',
                'properties': {
                    'density': 7.85,  # g/cm³
                    'tensile_strength': 400,  # MPa
                    'thermal_conductivity': 50.2,  # W/(m·K)
                    'electrical_conductivity': 5.8,  # MS/m
                    'melting_point': 1370,  # °C
                    'recyclability': 0.85  # 0-1 scale
                },
                'applications': ['construction', 'automotive', 'appliances', 'tools'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'very high',
                    'water_usage': 'high'
                },
                'processing_methods': ['casting', 'forging', 'rolling', 'welding'],
                'finish_options': ['galvanized', 'painted', 'powder-coated', 'chrome-plated'],
                'cost_factor': 0.5  # 0-1 scale, relative to category
            },
            
            # Plastics
            'abs_plastic': {
                'name': 'ABS Plastic',
                'category': 'plastics',
                'description': 'Thermoplastic polymer with good impact resistance and mechanical properties',
                'properties': {
                    'density': 1.05,  # g/cm³
                    'tensile_strength': 40,  # MPa
                    'thermal_conductivity': 0.17,  # W/(m·K)
                    'melting_point': 105,  # °C
                    'recyclability': 0.6,  # 0-1 scale
                    'biodegradability': 0.1  # 0-1 scale
                },
                'applications': ['electronics', 'automotive', 'toys', '3D printing'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': False,
                    'renewable': False,
                    'carbon_footprint': 'medium',
                    'water_usage': 'low'
                },
                'processing_methods': ['injection molding', 'extrusion', '3D printing', 'thermoforming'],
                'finish_options': ['smooth', 'textured', 'painted', 'chrome-plated'],
                'cost_factor': 0.4  # 0-1 scale, relative to category
            },
            'polypropylene': {
                'name': 'Polypropylene',
                'category': 'plastics',
                'description': 'Versatile thermoplastic polymer with good chemical resistance and fatigue resistance',
                'properties': {
                    'density': 0.9,  # g/cm³
                    'tensile_strength': 35,  # MPa
                    'thermal_conductivity': 0.22,  # W/(m·K)
                    'melting_point': 160,  # °C
                    'recyclability': 0.7,  # 0-1 scale
                    'biodegradability': 0.2  # 0-1 scale
                },
                'applications': ['packaging', 'textiles', 'automotive', 'medical'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': False,
                    'renewable': False,
                    'carbon_footprint': 'medium',
                    'water_usage': 'low'
                },
                'processing_methods': ['injection molding', 'blow molding', 'thermoforming', 'extrusion'],
                'finish_options': ['smooth', 'textured', 'matte', 'glossy'],
                'cost_factor': 0.3  # 0-1 scale, relative to category
            },
            
            # Woods
            'oak': {
                'name': 'Oak',
                'category': 'woods',
                'description': 'Hard, durable hardwood with prominent grain patterns',
                'properties': {
                    'density': 0.75,  # g/cm³
                    'hardness': 1360,  # Janka hardness
                    'moisture_content': 0.08,  # typical 8%
                    'grain_pattern': 'prominent',
                    'sustainability': 0.7,  # 0-1 scale
                    'workability': 0.6  # 0-1 scale
                },
                'applications': ['furniture', 'flooring', 'cabinetry', 'construction'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': False,
                    'renewable': True,
                    'carbon_footprint': 'low',
                    'water_usage': 'low'
                },
                'processing_methods': ['sawing', 'planing', 'sanding', 'turning'],
                'finish_options': ['stained', 'oiled', 'varnished', 'painted'],
                'cost_factor': 0.7  # 0-1 scale, relative to category
            },
            'bamboo': {
                'name': 'Bamboo',
                'category': 'woods',
                'description': 'Fast-growing grass with wood-like characteristics and excellent sustainability',
                'properties': {
                    'density': 0.6,  # g/cm³
                    'hardness': 1380,  # Janka hardness
                    'moisture_content': 0.06,  # typical 6%
                    'grain_pattern': 'distinctive',
                    'sustainability': 0.95,  # 0-1 scale
                    'workability': 0.7  # 0-1 scale
                },
                'applications': ['flooring', 'furniture', 'utensils', 'decorative'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': False,
                    'renewable': True,
                    'carbon_footprint': 'very low',
                    'water_usage': 'low'
                },
                'processing_methods': ['laminating', 'pressing', 'cutting', 'sanding'],
                'finish_options': ['natural', 'carbonized', 'stained', 'sealed'],
                'cost_factor': 0.6  # 0-1 scale, relative to category
            },
            
            # Textiles
            'cotton': {
                'name': 'Cotton',
                'category': 'textiles',
                'description': 'Natural fiber that produces soft, breathable fabric',
                'properties': {
                    'weight': 0.15,  # g/cm²
                    'strength': 0.4,  # 0-1 scale
                    'elasticity': 0.3,  # 0-1 scale
                    'breathability': 0.9,  # 0-1 scale
                    'water_resistance': 0.2,  # 0-1 scale
                    'sustainability': 0.7  # 0-1 scale
                },
                'applications': ['clothing', 'bedding', 'upholstery', 'medical'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': False,
                    'renewable': True,
                    'carbon_footprint': 'low',
                    'water_usage': 'very high'
                },
                'processing_methods': ['spinning', 'weaving', 'knitting', 'dyeing'],
                'finish_options': ['natural', 'dyed', 'printed', 'treated'],
                'cost_factor': 0.5  # 0-1 scale, relative to category
            },
            'polyester': {
                'name': 'Polyester',
                'category': 'textiles',
                'description': 'Synthetic fiber known for durability and wrinkle resistance',
                'properties': {
                    'weight': 0.13,  # g/cm²
                    'strength': 0.7,  # 0-1 scale
                    'elasticity': 0.5,  # 0-1 scale
                    'breathability': 0.3,  # 0-1 scale
                    'water_resistance': 0.7,  # 0-1 scale
                    'sustainability': 0.4  # 0-1 scale
                },
                'applications': ['clothing', 'upholstery', 'industrial', 'outdoor'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'high',
                    'water_usage': 'medium'
                },
                'processing_methods': ['spinning', 'weaving', 'knitting', 'heat-setting'],
                'finish_options': ['dyed', 'printed', 'brushed', 'waterproof'],
                'cost_factor': 0.3  # 0-1 scale, relative to category
            },
            
            # Ceramics
            'porcelain': {
                'name': 'Porcelain',
                'category': 'ceramics',
                'description': 'Fine ceramic material known for its strength, whiteness, and translucency',
                'properties': {
                    'density': 2.4,  # g/cm³
                    'hardness': 7,  # Mohs scale
                    'thermal_conductivity': 1.5,  # W/(m·K)
                    'electrical_resistivity': 10e12,  # Ω·m
                    'brittleness': 0.8,  # 0-1 scale
                    'heat_resistance': 0.9  # 0-1 scale
                },
                'applications': ['tableware', 'decorative', 'electrical', 'dental'],
                'sustainability': {
                    'recyclable': False,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'high',
                    'water_usage': 'medium'
                },
                'processing_methods': ['slip casting', 'throwing', 'pressing', 'firing'],
                'finish_options': ['glazed', 'unglazed', 'painted', 'gilded'],
                'cost_factor': 0.7  # 0-1 scale, relative to category
            },
            
            # Composites
            'carbon_fiber': {
                'name': 'Carbon Fiber Composite',
                'category': 'composites',
                'description': 'Lightweight, high-strength composite material with carbon fiber reinforcement',
                'properties': {
                    'density': 1.6,  # g/cm³
                    'strength_to_weight_ratio': 0.95,  # 0-1 scale
                    'stiffness': 0.9,  # 0-1 scale
                    'fatigue_resistance': 0.85,  # 0-1 scale
                    'corrosion_resistance': 0.9,  # 0-1 scale
                    'customizability': 0.8  # 0-1 scale
                },
                'applications': ['aerospace', 'automotive', 'sports', 'marine'],
                'sustainability': {
                    'recyclable': False,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'very high',
                    'water_usage': 'medium'
                },
                'processing_methods': ['layup', 'resin transfer', 'filament winding', 'pultrusion'],
                'finish_options': ['clear coat', 'painted', 'matte', 'polished'],
                'cost_factor': 0.9  # 0-1 scale, relative to category
            },
            
            # Glass
            'soda_lime_glass': {
                'name': 'Soda-Lime Glass',
                'category': 'glass',
                'description': 'Common glass type used for windows, containers, and everyday items',
                'properties': {
                    'density': 2.5,  # g/cm³
                    'refractive_index': 1.52,
                    'transparency': 0.9,  # 0-1 scale
                    'thermal_conductivity': 1.0,  # W/(m·K)
                    'brittleness': 0.85,  # 0-1 scale
                    'recyclability': 0.9  # 0-1 scale
                },
                'applications': ['windows', 'containers', 'tableware', 'decorative'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'medium',
                    'water_usage': 'low'
                },
                'processing_methods': ['blowing', 'casting', 'floating', 'pressing'],
                'finish_options': ['clear', 'frosted', 'tinted', 'patterned'],
                'cost_factor': 0.4  # 0-1 scale, relative to category
            },
            
            # Natural Materials
            'cork': {
                'name': 'Cork',
                'category': 'natural_materials',
                'description': 'Natural, sustainable material harvested from cork oak trees',
                'properties': {
                    'density': 0.24,  # g/cm³
                    'biodegradability': 0.9,  # 0-1 scale
                    'sustainability': 0.95,  # 0-1 scale
                    'renewability': 0.9,  # 0-1 scale
                    'processing_requirements': 0.3,  # 0-1 scale
                    'durability': 0.7  # 0-1 scale
                },
                'applications': ['flooring', 'insulation', 'accessories', 'packaging'],
                'sustainability': {
                    'recyclable': True,
                    'energy_intensive': False,
                    'renewable': True,
                    'carbon_footprint': 'very low',
                    'water_usage': 'very low'
                },
                'processing_methods': ['cutting', 'pressing', 'grinding', 'molding'],
                'finish_options': ['natural', 'stained', 'sealed', 'painted'],
                'cost_factor': 0.6  # 0-1 scale, relative to category
            },
            
            # Synthetic Materials
            'silicone': {
                'name': 'Silicone',
                'category': 'synthetic_materials',
                'description': 'Flexible, heat-resistant polymer with rubber-like properties',
                'properties': {
                    'density': 1.1,  # g/cm³
                    'durability': 0.85,  # 0-1 scale
                    'chemical_resistance': 0.9,  # 0-1 scale
                    'customizability': 0.8,  # 0-1 scale
                    'production_cost': 0.6,  # 0-1 scale
                    'environmental_impact': 0.5  # 0-1 scale
                },
                'applications': ['kitchenware', 'medical', 'electronics', 'sealants'],
                'sustainability': {
                    'recyclable': False,
                    'energy_intensive': True,
                    'renewable': False,
                    'carbon_footprint': 'medium',
                    'water_usage': 'low'
                },
                'processing_methods': ['injection molding', 'extrusion', 'compression molding', 'casting'],
                'finish_options': ['matte', 'glossy', 'textured', 'colored'],
                'cost_factor': 0.7  # 0-1 scale, relative to category
            }
        }
        
        logger.info(f"Initialized default material database with {len(self.materials)} materials")
    
    def save_database(self, output_path=None):
        """
        Save the material database to a file.
        
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
                    'materials': self.materials,
                    'categories': self.categories,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"Saved material database to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving material database: {str(e)}")
            return False
    
    def get_material(self, material_id):
        """
        Get information about a specific material.
        
        Args:
            material_id (str): Material identifier
            
        Returns:
            dict: Material information
        """
        return self.materials.get(material_id, None)
    
    def get_materials_by_category(self, category):
        """
        Get all materials in a specific category.
        
        Args:
            category (str): Material category
            
        Returns:
            dict: Materials in the category
        """
        return {k: v for k, v in self.materials.items() if v.get('category') == category}
    
    def get_materials_by_property(self, property_name, min_value=None, max_value=None):
        """
        Get materials that match specific property criteria.
        
        Args:
            property_name (str): Property to filter by
            min_value (float, optional): Minimum property value
            max_value (float, optional): Maximum property value
            
        Returns:
            dict: Materials matching the criteria
        """
        result = {}
        
        for material_id, material in self.materials.items():
            properties = material.get('properties', {})
            if property_name in properties:
                value = properties[property_name]
                
                # Check if value is within range
                if (min_value is None or value >= min_value) and (max_value is None or value <= max_value):
                    result[material_id] = material
        
        return result
    
    def get_materials_by_application(self, application):
        """
        Get materials suitable for a specific application.
        
        Args:
            application (str): Application to filter by
            
        Returns:
            dict: Materials suitable for the application
        """
        return {k: v for k, v in self.materials.items() if application in v.get('applications', [])}
    
    def get_sustainable_materials(self, min_score=0.7):
        """
        Get materials with high sustainability scores.
        
        Args:
            min_score (float): Minimum sustainability score (0-1)
            
        Returns:
            dict: Sustainable materials
        """
        result = {}
        
        for material_id, material in self.materials.items():
            # Check sustainability in properties
            properties = material.get('properties', {})
            if 'sustainability' in properties and properties['sustainability'] >= min_score:
                result[material_id] = material
                continue
            
            # Check sustainability info
            sustainability = material.get('sustainability', {})
            if sustainability.get('renewable', False) and sustainability.get('carbon_footprint', '') in ['low', 'very low']:
                result[material_id] = material
        
        return result
    
    def get_material_compatibility(self, material_id1, material_id2):
        """
        Determine compatibility between two materials.
        
        Args:
            material_id1 (str): First material identifier
            material_id2 (str): Second material identifier
            
        Returns:
            dict: Compatibility information
        """
        material1 = self.get_material(material_id1)
        material2 = self.get_material(material_id2)
        
        if not material1 or not material2:
            return {'compatible': False, 'reason': 'One or both materials not found'}
        
        # Check if materials are in the same category
        same_category = material1.get('category') == material2.get('category')
        
        # Check for known incompatible combinations
        incompatible_pairs = [
            ('metals', 'ceramics'),  # Different thermal expansion
            ('woods', 'metals')  # Moisture issues
        ]
        
        category_pair = (material1.get('category'), material2.get('category'))
        category_pair_reversed = (material2.get('category'), material1.get('category'))
        
        incompatible = category_pair in incompatible_pairs or category_pair_reversed in incompatible_pairs
        
        # Determine compatibility score (0-1)
        compatibility_score = 0.8 if same_category else 0.5
        if incompatible:
            compatibility_score = 0.2
        
        # Generate compatibility information
        compatibility = {
            'compatible': compatibility_score > 0.5,
            'score': compatibility_score,
            'same_category': same_category,
            'considerations': []
        }
        
        # Add considerations based on material properties
        if 'metals' in [material1.get('category'), material2.get('category')]:
            compatibility['considerations'].append('Consider galvanic corrosion when combining different metals')
        
        if 'woods' in [material1.get('category'), material2.get('category')]:
            compatibility['considerations'].append('Consider moisture expansion/contraction of wood')
        
        if material1.get('properties', {}).get('thermal_conductivity', 0) > 100 and material2.get('properties', {}).get('thermal_conductivity', 0) < 1:
            compatibility['considerations'].append('Large difference in thermal conductivity may cause issues with temperature changes')
        
        return compatibility
    
    def suggest_alternative_materials(self, material_id, eco_friendly=False, cost_effective=False, performance=False):
        """
        Suggest alternative materials with similar or better properties.
        
        Args:
            material_id (str): Reference material identifier
            eco_friendly (bool): Prioritize eco-friendly alternatives
            cost_effective (bool): Prioritize cost-effective alternatives
            performance (bool): Prioritize performance
            
        Returns:
            list: Suggested alternative materials
        """
        material = self.get_material(material_id)
        if not material:
            return []
        
        category = material.get('category')
        similar_materials = self.get_materials_by_category(category)
        
        # Remove the reference material
        if material_id in similar_materials:
            del similar_materials[material_id]
        
        # Score alternatives based on criteria
        scored_alternatives = []
        
        for alt_id, alt_material in similar_materials.items():
            score = 0
            
            # Base similarity score
            score += 0.5
            
            # Eco-friendly score
            if eco_friendly:
                alt_sustainability = alt_material.get('sustainability', {})
                if alt_sustainability.get('recyclable', False):
                    score += 0.2
                if alt_sustainability.get('renewable', False):
                    score += 0.2
                if alt_sustainability.get('carbon_footprint', '') in ['low', 'very low']:
                    score += 0.2
            
            # Cost-effective score
            if cost_effective:
                ref_cost = material.get('cost_factor', 0.5)
                alt_cost = alt_material.get('cost_factor', 0.5)
                if alt_cost < ref_cost:
                    score += 0.3 * (ref_cost - alt_cost) / ref_cost
            
            # Performance score
            if performance:
                # Compare key properties
                ref_props = material.get('properties', {})
                alt_props = alt_material.get('properties', {})
                
                # Check common properties
                common_props = set(ref_props.keys()).intersection(set(alt_props.keys()))
                if common_props:
                    better_props = 0
                    for prop in common_props:
                        # For some properties, higher is better
                        higher_better = prop in ['strength', 'durability', 'recyclability', 'sustainability']
                        
                        if higher_better and alt_props[prop] > ref_props[prop]:
                            better_props += 1
                        elif not higher_better and alt_props[prop] < ref_props[prop]:
                            better_props += 1
                    
                    score += 0.3 * (better_props / len(common_props))
            
            scored_alternatives.append({
                'id': alt_id,
                'name': alt_material.get('name'),
                'score': score,
                'material': alt_material
            })
        
        # Sort by score (descending)
        scored_alternatives.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top alternatives
        return scored_alternatives[:5]
    
    def get_material_for_industry(self, industry, application=None, eco_friendly=False):
        """
        Get recommended materials for a specific industry and application.
        
        Args:
            industry (str): Industry (e.g., 'furniture', 'electronics')
            application (str, optional): Specific application
            eco_friendly (bool): Whether to prioritize eco-friendly materials
            
        Returns:
            list: Recommended materials
        """
        # Define industry-specific material recommendations
        industry_materials = {
            'furniture': ['oak', 'bamboo', 'steel', 'aluminum', 'polypropylene'],
            'electronics': ['abs_plastic', 'aluminum', 'silicone', 'polypropylene'],
            'packaging': ['polypropylene', 'soda_lime_glass', 'cork', 'paper'],
            'fashion': ['cotton', 'polyester', 'leather', 'silicone'],
            'construction': ['steel', 'aluminum', 'concrete', 'oak', 'bamboo'],
            'automotive': ['steel', 'aluminum', 'carbon_fiber', 'abs_plastic', 'leather'],
            'medical': ['silicone', 'abs_plastic', 'stainless_steel', 'cotton'],
            'home_goods': ['porcelain', 'soda_lime_glass', 'bamboo', 'cotton', 'silicone']
        }
        
        # Get materials for the industry
        material_ids = industry_materials.get(industry, [])
        
        # Filter by application if specified
        if application:
            material_ids = [m_id for m_id in material_ids if m_id in self.materials and 
                           application in self.materials[m_id].get('applications', [])]
        
        # Get material details
        recommended_materials = []
        for material_id in material_ids:
            material = self.get_material(material_id)
            if material:
                # Calculate recommendation score
                score = 0.7  # Base score
                
                # Adjust score based on eco-friendliness if requested
                if eco_friendly:
                    sustainability = material.get('sustainability', {})
                    if sustainability.get('recyclable', False):
                        score += 0.1
                    if sustainability.get('renewable', False):
                        score += 0.1
                    if sustainability.get('carbon_footprint', '') in ['low', 'very low']:
                        score += 0.1
                
                recommended_materials.append({
                    'id': material_id,
                    'name': material.get('name'),
                    'score': score,
                    'material': material
                })
        
        # Sort by score (descending)
        recommended_materials.sort(key=lambda x: x['score'], reverse=True)
        
        return recommended_materials
    
    def add_material(self, material_id, material_data):
        """
        Add a new material to the database.
        
        Args:
            material_id (str): Material identifier
            material_data (dict): Material information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate material data
            required_fields = ['name', 'category', 'description', 'properties']
            for field in required_fields:
                if field not in material_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add material to database
            self.materials[material_id] = material_data
            logger.info(f"Added material: {material_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding material: {str(e)}")
            return False
    
    def update_material(self, material_id, material_data):
        """
        Update an existing material in the database.
        
        Args:
            material_id (str): Material identifier
            material_data (dict): Updated material information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if material_id not in self.materials:
                logger.error(f"Material not found: {material_id}")
                return False
            
            # Update material data
            self.materials[material_id].update(material_data)
            logger.info(f"Updated material: {material_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating material: {str(e)}")
            return False
    
    def delete_material(self, material_id):
        """
        Delete a material from the database.
        
        Args:
            material_id (str): Material identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if material_id not in self.materials:
                logger.error(f"Material not found: {material_id}")
                return False
            
            # Delete material
            del self.materials[material_id]
            logger.info(f"Deleted material: {material_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting material: {str(e)}")
            return False


if __name__ == "__main__":
    # Example usage
    database = MaterialDatabase()
    
    # Get materials by category
    metals = database.get_materials_by_category('metals')
    print(f"Found {len(metals)} metals")
    
    # Get sustainable materials
    sustainable = database.get_sustainable_materials()
    print(f"Found {len(sustainable)} sustainable materials")
    
    # Get material compatibility
    compatibility = database.get_material_compatibility('aluminum', 'oak')
    print(f"Compatibility: {compatibility}")
    
    # Suggest alternative materials
    alternatives = database.suggest_alternative_materials('oak', eco_friendly=True)
    print(f"Suggested alternatives: {[alt['name'] for alt in alternatives]}")
    
    # Get materials for industry
    furniture_materials = database.get_material_for_industry('furniture', eco_friendly=True)
    print(f"Recommended materials for furniture: {[mat['name'] for mat in furniture_materials]}")
