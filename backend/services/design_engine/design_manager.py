import logging
import json
import os
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DesignManager:
    """
    Core design manager class that integrates all design engine components.
    Provides cross-industry design capabilities, material-specific design features,
    and coordinates the design process across various product types.
    """
    
    def __init__(self, material_service=None, standards_service=None, 
                 sustainability_service=None, trend_service=None, 
                 compliance_service=None, database_path=None):
        """
        Initialize the DesignManager.
        
        Args:
            material_service: Reference to the MaterialDatabase service
            standards_service: Reference to the IndustryStandards service
            sustainability_service: Reference to the SustainabilityAnalyzer service
            trend_service: Reference to the TrendAnalyzer service
            compliance_service: Reference to the ComplianceChecker service
            database_path (str, optional): Path to the design manager database file
        """
        logger.info("Initializing DesignManager")
        self.material_service = material_service
        self.standards_service = standards_service
        self.sustainability_service = sustainability_service
        self.trend_service = trend_service
        self.compliance_service = compliance_service
        self.database_path = database_path
        self.design_templates = {}
        self.industry_configs = {}
        self.design_projects = {}
        self._load_design_data()
    
    def _load_design_data(self):
        """
        Load design data from database file or initialize with default data.
        """
        try:
            if self.database_path and os.path.exists(self.database_path):
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    self.design_templates = data.get('design_templates', {})
                    self.industry_configs = data.get('industry_configs', {})
                    self.design_projects = data.get('design_projects', {})
                logger.info(f"Loaded design data from database")
            else:
                logger.info("Initializing default design database")
                self._initialize_default_data()
        except Exception as e:
            logger.error(f"Error loading design data: {str(e)}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """
        Initialize the database with default design data.
        """
        # Initialize design templates for different industries
        self.design_templates = {
            'furniture': {
                'chair': {
                    'name': 'Chair Template',
                    'description': 'Basic template for chair design',
                    'components': [
                        {
                            'name': 'Seat',
                            'required': True,
                            'default_materials': ['wood', 'plastic', 'upholstery'],
                            'properties': {
                                'dimensions': {'width': 45, 'depth': 45, 'height': 5},
                                'load_capacity': 120,
                                'ergonomic_factors': ['contour', 'padding']
                            }
                        },
                        {
                            'name': 'Backrest',
                            'required': True,
                            'default_materials': ['wood', 'plastic', 'upholstery'],
                            'properties': {
                                'dimensions': {'width': 45, 'height': 40, 'thickness': 3},
                                'ergonomic_factors': ['lumbar_support', 'angle']
                            }
                        },
                        {
                            'name': 'Legs/Base',
                            'required': True,
                            'default_materials': ['wood', 'metal', 'plastic'],
                            'properties': {
                                'dimensions': {'height': 45},
                                'load_capacity': 150,
                                'stability_factors': ['base_width', 'foot_design']
                            }
                        },
                        {
                            'name': 'Armrests',
                            'required': False,
                            'default_materials': ['wood', 'metal', 'plastic', 'upholstery'],
                            'properties': {
                                'dimensions': {'length': 30, 'width': 5, 'height': 20},
                                'ergonomic_factors': ['height_adjustable', 'padding']
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['modern', 'traditional', 'minimalist', 'industrial'],
                        'use_case': ['dining', 'office', 'lounge', 'outdoor'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['assembly', 'upholstery', 'woodworking', 'injection_molding'],
                    'applicable_standards': ['ANSI/BIFMA X5.1', 'EN 1728', 'EN 16139']
                },
                'table': {
                    'name': 'Table Template',
                    'description': 'Basic template for table design',
                    'components': [
                        {
                            'name': 'Tabletop',
                            'required': True,
                            'default_materials': ['wood', 'glass', 'metal', 'stone'],
                            'properties': {
                                'dimensions': {'width': 120, 'depth': 80, 'thickness': 3},
                                'load_capacity': 100,
                                'surface_properties': ['finish', 'texture', 'edge_profile']
                            }
                        },
                        {
                            'name': 'Legs/Base',
                            'required': True,
                            'default_materials': ['wood', 'metal', 'plastic'],
                            'properties': {
                                'dimensions': {'height': 75},
                                'load_capacity': 150,
                                'stability_factors': ['base_width', 'foot_design']
                            }
                        },
                        {
                            'name': 'Stretchers',
                            'required': False,
                            'default_materials': ['wood', 'metal'],
                            'properties': {
                                'dimensions': {'length': 80, 'width': 3, 'height': 3},
                                'structural_properties': ['rigidity', 'connection_type']
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['modern', 'traditional', 'minimalist', 'industrial'],
                        'use_case': ['dining', 'coffee', 'work', 'outdoor'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['assembly', 'woodworking', 'metal_fabrication', 'glass_processing'],
                    'applicable_standards': ['ANSI/BIFMA X5.5', 'EN 1730']
                }
            },
            'packaging': {
                'box': {
                    'name': 'Box Template',
                    'description': 'Basic template for box packaging design',
                    'components': [
                        {
                            'name': 'Box Body',
                            'required': True,
                            'default_materials': ['cardboard', 'corrugated_board', 'paperboard'],
                            'properties': {
                                'dimensions': {'width': 20, 'depth': 20, 'height': 20},
                                'strength': {'stacking': 50, 'burst': 200},
                                'surface_properties': ['printability', 'finish', 'coating']
                            }
                        },
                        {
                            'name': 'Closure',
                            'required': True,
                            'default_materials': ['adhesive', 'tuck_flap'],
                            'properties': {
                                'security_level': 'standard',
                                'reusability': False
                            }
                        },
                        {
                            'name': 'Inner Packaging',
                            'required': False,
                            'default_materials': ['paper_pulp', 'foam', 'bubble_wrap'],
                            'properties': {
                                'cushioning_level': 'medium',
                                'recyclability': True
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['standard', 'premium', 'eco-friendly', 'minimalist'],
                        'use_case': ['shipping', 'retail', 'gift', 'food'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium']
                    },
                    'manufacturing_processes': ['die_cutting', 'folding', 'gluing', 'printing'],
                    'applicable_standards': ['ISO 3394', 'ISTA 3A', 'ASTM D4169']
                },
                'bottle': {
                    'name': 'Bottle Template',
                    'description': 'Basic template for bottle packaging design',
                    'components': [
                        {
                            'name': 'Bottle Body',
                            'required': True,
                            'default_materials': ['plastic', 'glass', 'metal', 'bioplastic'],
                            'properties': {
                                'dimensions': {'height': 20, 'diameter': 6},
                                'volume': 500,
                                'transparency': 'transparent',
                                'barrier_properties': ['moisture', 'oxygen', 'light']
                            }
                        },
                        {
                            'name': 'Cap/Closure',
                            'required': True,
                            'default_materials': ['plastic', 'metal', 'bioplastic'],
                            'properties': {
                                'type': ['screw', 'flip-top', 'pump', 'spray'],
                                'tamper_evident': True,
                                'child_resistant': False
                            }
                        },
                        {
                            'name': 'Label',
                            'required': True,
                            'default_materials': ['paper', 'plastic_film', 'direct_print'],
                            'properties': {
                                'dimensions': {'height': 10, 'width': 15},
                                'adhesive_type': 'permanent',
                                'printability': 'high'
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['standard', 'premium', 'eco-friendly', 'minimalist'],
                        'use_case': ['beverage', 'personal_care', 'household', 'food'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['blow_molding', 'injection_molding', 'glass_forming', 'labeling'],
                    'applicable_standards': ['ISO 22000', 'ASTM D2659', 'CFR Title 21']
                }
            },
            'electronics': {
                'enclosure': {
                    'name': 'Electronic Enclosure Template',
                    'description': 'Basic template for electronic device enclosure design',
                    'components': [
                        {
                            'name': 'Main Body',
                            'required': True,
                            'default_materials': ['plastic', 'metal', 'composite'],
                            'properties': {
                                'dimensions': {'width': 15, 'depth': 10, 'height': 3},
                                'protection_rating': 'IP54',
                                'thermal_properties': ['heat_dissipation', 'insulation'],
                                'electromagnetic_shielding': True
                            }
                        },
                        {
                            'name': 'Cover/Lid',
                            'required': True,
                            'default_materials': ['plastic', 'metal', 'composite'],
                            'properties': {
                                'dimensions': {'width': 15, 'depth': 10, 'thickness': 0.2},
                                'closure_type': ['snap_fit', 'screws', 'hinged'],
                                'transparency': 'opaque'
                            }
                        },
                        {
                            'name': 'Interface Panel',
                            'required': True,
                            'default_materials': ['plastic', 'metal', 'glass'],
                            'properties': {
                                'dimensions': {'width': 5, 'height': 3},
                                'interface_elements': ['buttons', 'display', 'ports', 'indicators'],
                                'accessibility': 'front'
                            }
                        },
                        {
                            'name': 'Internal Mounting',
                            'required': True,
                            'default_materials': ['plastic', 'metal'],
                            'properties': {
                                'mounting_type': ['standoffs', 'rails', 'brackets'],
                                'component_compatibility': ['PCB', 'battery', 'display']
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['industrial', 'consumer', 'medical', 'rugged'],
                        'use_case': ['portable', 'desktop', 'wall_mount', 'embedded'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'specialized']
                    },
                    'manufacturing_processes': ['injection_molding', 'die_casting', 'sheet_metal_forming', 'machining'],
                    'applicable_standards': ['IEC 60529', 'UL 94', 'IEC 61000', 'RoHS']
                },
                'wearable': {
                    'name': 'Wearable Device Template',
                    'description': 'Basic template for wearable electronic device design',
                    'components': [
                        {
                            'name': 'Main Body',
                            'required': True,
                            'default_materials': ['plastic', 'metal', 'silicone', 'composite'],
                            'properties': {
                                'dimensions': {'width': 4, 'depth': 1, 'height': 4},
                                'protection_rating': 'IP67',
                                'weight': 50,
                                'ergonomic_factors': ['comfort', 'weight_distribution']
                            }
                        },
                        {
                            'name': 'Strap/Attachment',
                            'required': True,
                            'default_materials': ['silicone', 'fabric', 'leather', 'metal'],
                            'properties': {
                                'dimensions': {'length': 25, 'width': 2, 'thickness': 0.2},
                                'adjustability': True,
                                'closure_type': ['buckle', 'clasp', 'magnetic', 'hook_loop']
                            }
                        },
                        {
                            'name': 'Interface',
                            'required': True,
                            'default_materials': ['glass', 'plastic', 'touch_sensor'],
                            'properties': {
                                'dimensions': {'width': 3, 'height': 3},
                                'interface_type': ['touchscreen', 'buttons', 'gesture', 'voice'],
                                'display_type': ['OLED', 'LCD', 'e-ink']
                            }
                        },
                        {
                            'name': 'Sensors',
                            'required': True,
                            'default_materials': ['electronic_components'],
                            'properties': {
                                'sensor_types': ['accelerometer', 'heart_rate', 'temperature', 'gps'],
                                'accuracy': 'high',
                                'power_consumption': 'low'
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['sporty', 'casual', 'professional', 'medical'],
                        'use_case': ['fitness', 'health_monitoring', 'communication', 'navigation'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['injection_molding', 'die_casting', 'pcb_assembly', 'overmolding'],
                    'applicable_standards': ['IEC 60601', 'IP67', 'Bluetooth SIG', 'FCC Part 15']
                }
            },
            'fashion': {
                'shirt': {
                    'name': 'Shirt Template',
                    'description': 'Basic template for shirt design',
                    'components': [
                        {
                            'name': 'Body',
                            'required': True,
                            'default_materials': ['cotton', 'polyester', 'linen', 'silk'],
                            'properties': {
                                'dimensions': {'chest': 100, 'length': 70, 'shoulder': 45},
                                'fit_type': ['regular', 'slim', 'relaxed', 'oversized'],
                                'construction': ['seam_type', 'hem_style', 'dart_placement']
                            }
                        },
                        {
                            'name': 'Sleeves',
                            'required': True,
                            'default_materials': ['cotton', 'polyester', 'linen', 'silk'],
                            'properties': {
                                'dimensions': {'length': 60, 'width': 40},
                                'style': ['long', 'short', 'three_quarter', 'sleeveless'],
                                'cuff_type': ['button', 'french', 'elastic', 'none']
                            }
                        },
                        {
                            'name': 'Collar',
                            'required': True,
                            'default_materials': ['cotton', 'polyester', 'linen', 'silk'],
                            'properties': {
                                'dimensions': {'height': 5, 'points': 7},
                                'style': ['point', 'button_down', 'spread', 'mandarin', 'none'],
                                'stiffness': ['soft', 'medium', 'stiff']
                            }
                        },
                        {
                            'name': 'Fastening',
                            'required': True,
                            'default_materials': ['buttons', 'snaps', 'zipper', 'none'],
                            'properties': {
                                'type': ['center_front', 'offset', 'pullover'],
                                'closure_count': 7,
                                'placket_style': ['standard', 'hidden', 'decorative']
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['casual', 'formal', 'business', 'athletic'],
                        'use_case': ['everyday', 'work', 'special_occasion', 'performance'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['cutting', 'sewing', 'pressing', 'finishing'],
                    'applicable_standards': ['ASTM D6193', 'ISO 3758', 'AATCC 135']
                },
                'bag': {
                    'name': 'Bag Template',
                    'description': 'Basic template for bag design',
                    'components': [
                        {
                            'name': 'Main Compartment',
                            'required': True,
                            'default_materials': ['leather', 'canvas', 'nylon', 'polyester'],
                            'properties': {
                                'dimensions': {'width': 40, 'height': 30, 'depth': 15},
                                'volume': 18,
                                'closure_type': ['zipper', 'magnetic', 'drawstring', 'flap']
                            }
                        },
                        {
                            'name': 'Handles/Straps',
                            'required': True,
                            'default_materials': ['leather', 'canvas', 'nylon', 'webbing'],
                            'properties': {
                                'dimensions': {'length': 60, 'width': 2.5, 'thickness': 0.5},
                                'style': ['top_handle', 'shoulder', 'crossbody', 'backpack'],
                                'adjustability': True,
                                'attachment_type': ['stitched', 'riveted', 'hardware']
                            }
                        },
                        {
                            'name': 'Pockets',
                            'required': False,
                            'default_materials': ['leather', 'canvas', 'nylon', 'polyester'],
                            'properties': {
                                'count': 3,
                                'placement': ['exterior', 'interior', 'side'],
                                'closure_type': ['zipper', 'magnetic', 'none']
                            }
                        },
                        {
                            'name': 'Hardware',
                            'required': True,
                            'default_materials': ['metal', 'plastic'],
                            'properties': {
                                'type': ['zippers', 'buckles', 'snaps', 'rings'],
                                'finish': ['gold', 'silver', 'brass', 'matte_black'],
                                'quality_grade': ['standard', 'premium', 'luxury']
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['casual', 'formal', 'sporty', 'minimalist'],
                        'use_case': ['everyday', 'work', 'travel', 'special_occasion'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['cutting', 'sewing', 'edge_finishing', 'hardware_installation'],
                    'applicable_standards': ['ASTM F2057', 'ISO 23910', 'ASTM D6193']
                }
            },
            'home_goods': {
                'lamp': {
                    'name': 'Lamp Template',
                    'description': 'Basic template for lamp design',
                    'components': [
                        {
                            'name': 'Base',
                            'required': True,
                            'default_materials': ['metal', 'ceramic', 'wood', 'glass'],
                            'properties': {
                                'dimensions': {'diameter': 20, 'height': 15},
                                'weight': 1.5,
                                'stability_factors': ['center_of_gravity', 'footprint']
                            }
                        },
                        {
                            'name': 'Stem/Body',
                            'required': True,
                            'default_materials': ['metal', 'wood', 'ceramic', 'plastic'],
                            'properties': {
                                'dimensions': {'height': 40, 'diameter': 3},
                                'style': ['straight', 'curved', 'adjustable', 'articulated'],
                                'cable_management': ['internal', 'external', 'concealed']
                            }
                        },
                        {
                            'name': 'Shade',
                            'required': True,
                            'default_materials': ['fabric', 'paper', 'metal', 'glass'],
                            'properties': {
                                'dimensions': {'diameter_top': 30, 'diameter_bottom': 40, 'height': 25},
                                'shape': ['drum', 'cone', 'bell', 'empire'],
                                'light_diffusion': ['opaque', 'translucent', 'transparent']
                            }
                        },
                        {
                            'name': 'Light Source',
                            'required': True,
                            'default_materials': ['led', 'incandescent', 'halogen', 'fluorescent'],
                            'properties': {
                                'type': ['bulb', 'integrated_led', 'strip'],
                                'wattage': 9,
                                'color_temperature': 3000,
                                'dimmable': True
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['modern', 'traditional', 'industrial', 'minimalist'],
                        'use_case': ['ambient', 'task', 'accent', 'decorative'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['metal_forming', 'woodworking', 'glass_blowing', 'wiring_assembly'],
                    'applicable_standards': ['UL 153', 'IEC 60598', 'Energy Star']
                },
                'vase': {
                    'name': 'Vase Template',
                    'description': 'Basic template for vase design',
                    'components': [
                        {
                            'name': 'Body',
                            'required': True,
                            'default_materials': ['ceramic', 'glass', 'metal', 'resin'],
                            'properties': {
                                'dimensions': {'height': 25, 'diameter': 15},
                                'shape': ['cylindrical', 'spherical', 'conical', 'organic'],
                                'volume': 2,
                                'water_tight': True
                            }
                        },
                        {
                            'name': 'Neck/Opening',
                            'required': True,
                            'default_materials': ['ceramic', 'glass', 'metal', 'resin'],
                            'properties': {
                                'dimensions': {'diameter': 8, 'height': 5},
                                'shape': ['round', 'flared', 'narrow', 'asymmetric'],
                                'functionality': ['flower_holding', 'decorative']
                            }
                        },
                        {
                            'name': 'Base',
                            'required': True,
                            'default_materials': ['ceramic', 'glass', 'metal', 'resin'],
                            'properties': {
                                'dimensions': {'diameter': 10, 'height': 2},
                                'stability': 'high',
                                'surface_protection': ['felt_pad', 'integrated', 'none']
                            }
                        },
                        {
                            'name': 'Surface Treatment',
                            'required': True,
                            'default_materials': ['glaze', 'paint', 'natural_finish', 'texture'],
                            'properties': {
                                'finish_type': ['glossy', 'matte', 'textured', 'metallic'],
                                'color_application': ['solid', 'gradient', 'pattern', 'multi_color'],
                                'water_resistance': True
                            }
                        }
                    ],
                    'design_parameters': {
                        'style': ['modern', 'traditional', 'minimalist', 'organic'],
                        'use_case': ['floral', 'decorative', 'functional', 'artistic'],
                        'sustainability_level': ['standard', 'eco-friendly', 'sustainable'],
                        'price_tier': ['budget', 'mid-range', 'premium', 'luxury']
                    },
                    'manufacturing_processes': ['pottery_throwing', 'glass_blowing', 'slip_casting', 'molding'],
                    'applicable_standards': ['ASTM C1027', 'ASTM C1378', 'ISO 10545']
                }
            }
        }
        
        # Initialize industry-specific configurations
        self.industry_configs = {
            'furniture': {
                'name': 'Furniture Design',
                'description': 'Configuration for furniture design',
                'design_principles': [
                    {
                        'name': 'Ergonomics',
                        'description': 'Design for human comfort and usability',
                        'key_considerations': [
                            'Anthropometric data',
                            'User comfort',
                            'Accessibility',
                            'Usability'
                        ]
                    },
                    {
                        'name': 'Structural Integrity',
                        'description': 'Design for stability and durability',
                        'key_considerations': [
                            'Load capacity',
                            'Stability',
                            'Joint strength',
                            'Material properties'
                        ]
                    },
                    {
                        'name': 'Manufacturability',
                        'description': 'Design for efficient production',
                        'key_considerations': [
                            'Material selection',
                            'Production processes',
                            'Assembly methods',
                            'Cost optimization'
                        ]
                    }
                ],
                'material_considerations': {
                    'wood': {
                        'properties': ['grain_direction', 'moisture_content', 'hardness'],
                        'processing_methods': ['sawing', 'planing', 'sanding', 'finishing'],
                        'joining_techniques': ['mortise_and_tenon', 'dovetail', 'dowels', 'screws']
                    },
                    'metal': {
                        'properties': ['strength', 'weight', 'corrosion_resistance'],
                        'processing_methods': ['cutting', 'bending', 'welding', 'finishing'],
                        'joining_techniques': ['welding', 'bolting', 'riveting', 'adhesives']
                    },
                    'upholstery': {
                        'properties': ['durability', 'comfort', 'appearance'],
                        'processing_methods': ['cutting', 'sewing', 'stretching', 'stapling'],
                        'joining_techniques': ['stitching', 'stapling', 'adhesives', 'zippers']
                    }
                },
                'design_constraints': {
                    'standard_dimensions': {
                        'chair_seat_height': {'min': 40, 'max': 50, 'unit': 'cm'},
                        'table_height': {'min': 70, 'max': 80, 'unit': 'cm'},
                        'desk_depth': {'min': 60, 'max': 80, 'unit': 'cm'}
                    },
                    'safety_requirements': [
                        'No sharp edges or corners',
                        'Stable under normal use',
                        'Non-toxic materials',
                        'Fire resistance for upholstery'
                    ],
                    'shipping_considerations': [
                        'Flat-pack capability',
                        'Weight limitations',
                        'Protection during transport',
                        'Assembly complexity'
                    ]
                }
            },
            'packaging': {
                'name': 'Packaging Design',
                'description': 'Configuration for packaging design',
                'design_principles': [
                    {
                        'name': 'Protection',
                        'description': 'Design for product protection during handling and transport',
                        'key_considerations': [
                            'Impact resistance',
                            'Moisture protection',
                            'Temperature stability',
                            'Vibration dampening'
                        ]
                    },
                    {
                        'name': 'Sustainability',
                        'description': 'Design for environmental responsibility',
                        'key_considerations': [
                            'Material reduction',
                            'Recyclability',
                            'Biodegradability',
                            'Reusability'
                        ]
                    },
                    {
                        'name': 'User Experience',
                        'description': 'Design for consumer interaction',
                        'key_considerations': [
                            'Ease of opening',
                            'Reclosability',
                            'Information clarity',
                            'Disposal instructions'
                        ]
                    }
                ],
                'material_considerations': {
                    'paper_based': {
                        'properties': ['grammage', 'stiffness', 'printability'],
                        'processing_methods': ['die_cutting', 'folding', 'gluing', 'printing'],
                        'environmental_impact': ['recyclability', 'biodegradability', 'sourcing']
                    },
                    'plastics': {
                        'properties': ['barrier_properties', 'transparency', 'flexibility'],
                        'processing_methods': ['thermoforming', 'injection_molding', 'blow_molding'],
                        'environmental_impact': ['recyclability', 'biodegradability', 'marine_impact']
                    },
                    'glass': {
                        'properties': ['clarity', 'weight', 'fragility'],
                        'processing_methods': ['molding', 'coating', 'labeling'],
                        'environmental_impact': ['recyclability', 'energy_intensity', 'weight']
                    }
                },
                'design_constraints': {
                    'standard_dimensions': {
                        'shipping_box': {'length': 60, 'width': 40, 'height': 40, 'unit': 'cm'},
                        'retail_shelf': {'depth': 30, 'height': 40, 'unit': 'cm'},
                        'pallet_optimization': {'length': 120, 'width': 100, 'unit': 'cm'}
                    },
                    'regulatory_requirements': [
                        'Material safety',
                        'Labeling requirements',
                        'Child-resistant features',
                        'Recycling symbols'
                    ],
                    'supply_chain_considerations': [
                        'Stackability',
                        'Cube utilization',
                        'Identification/tracking',
                        'Shelf life'
                    ]
                }
            },
            'electronics': {
                'name': 'Electronics Design',
                'description': 'Configuration for electronics product design',
                'design_principles': [
                    {
                        'name': 'Thermal Management',
                        'description': 'Design for heat dissipation and temperature control',
                        'key_considerations': [
                            'Heat generation',
                            'Cooling methods',
                            'Material conductivity',
                            'Airflow patterns'
                        ]
                    },
                    {
                        'name': 'Electromagnetic Compatibility',
                        'description': 'Design to minimize electromagnetic interference',
                        'key_considerations': [
                            'Shielding',
                            'Grounding',
                            'Component placement',
                            'Signal integrity'
                        ]
                    },
                    {
                        'name': 'User Interface',
                        'description': 'Design for intuitive user interaction',
                        'key_considerations': [
                            'Control placement',
                            'Feedback mechanisms',
                            'Accessibility',
                            'Intuitiveness'
                        ]
                    }
                ],
                'material_considerations': {
                    'enclosure_materials': {
                        'properties': ['thermal_conductivity', 'electromagnetic_shielding', 'durability'],
                        'processing_methods': ['injection_molding', 'die_casting', 'machining'],
                        'environmental_impact': ['recyclability', 'toxicity', 'energy_intensity']
                    },
                    'interface_materials': {
                        'properties': ['durability', 'tactile_feel', 'optical_clarity'],
                        'processing_methods': ['overmolding', 'printing', 'coating'],
                        'environmental_impact': ['recyclability', 'separability', 'toxicity']
                    },
                    'internal_components': {
                        'properties': ['reliability', 'performance', 'compatibility'],
                        'processing_methods': ['pcb_assembly', 'wire_harnessing', 'testing'],
                        'environmental_impact': ['hazardous_materials', 'recyclability', 'energy_consumption']
                    }
                },
                'design_constraints': {
                    'safety_requirements': [
                        'Electrical safety',
                        'Thermal safety',
                        'Battery safety',
                        'Sharp edge prevention'
                    ],
                    'regulatory_requirements': [
                        'EMC compliance',
                        'Energy efficiency',
                        'Hazardous substance restrictions',
                        'Recycling requirements'
                    ],
                    'manufacturing_considerations': [
                        'Design for assembly',
                        'Testability',
                        'Serviceability',
                        'Supply chain availability'
                    ]
                }
            },
            'fashion': {
                'name': 'Fashion Design',
                'description': 'Configuration for fashion product design',
                'design_principles': [
                    {
                        'name': 'Fit and Comfort',
                        'description': 'Design for proper fit and wearer comfort',
                        'key_considerations': [
                            'Body measurements',
                            'Movement allowance',
                            'Fabric properties',
                            'Seam placement'
                        ]
                    },
                    {
                        'name': 'Aesthetics',
                        'description': 'Design for visual appeal and style',
                        'key_considerations': [
                            'Silhouette',
                            'Proportion',
                            'Color theory',
                            'Texture combination'
                        ]
                    },
                    {
                        'name': 'Functionality',
                        'description': 'Design for intended use and performance',
                        'key_considerations': [
                            'End use requirements',
                            'Durability',
                            'Care and maintenance',
                            'Adaptability'
                        ]
                    }
                ],
                'material_considerations': {
                    'textiles': {
                        'properties': ['fiber_content', 'weight', 'drape', 'stretch'],
                        'processing_methods': ['cutting', 'sewing', 'finishing', 'printing'],
                        'environmental_impact': ['water_usage', 'chemical_usage', 'biodegradability']
                    },
                    'trims': {
                        'properties': ['durability', 'appearance', 'functionality'],
                        'processing_methods': ['application', 'finishing', 'testing'],
                        'environmental_impact': ['recyclability', 'toxicity', 'separability']
                    },
                    'hardware': {
                        'properties': ['strength', 'appearance', 'corrosion_resistance'],
                        'processing_methods': ['casting', 'plating', 'assembly'],
                        'environmental_impact': ['recyclability', 'toxicity', 'durability']
                    }
                },
                'design_constraints': {
                    'sizing_standards': {
                        'women': {'XS': [80, 60, 88], 'S': [84, 64, 92], 'M': [88, 68, 96], 'L': [92, 72, 100]},
                        'men': {'S': [90, 78, 94], 'M': [94, 82, 98], 'L': [98, 86, 102], 'XL': [102, 90, 106]},
                        'measurement_points': ['chest/bust', 'waist', 'hip']
                    },
                    'regulatory_requirements': [
                        'Fiber content labeling',
                        'Care instructions',
                        'Country of origin',
                        'Flammability standards'
                    ],
                    'production_considerations': [
                        'Pattern efficiency',
                        'Seam allowances',
                        'Construction methods',
                        'Grading rules'
                    ]
                }
            },
            'home_goods': {
                'name': 'Home Goods Design',
                'description': 'Configuration for home goods product design',
                'design_principles': [
                    {
                        'name': 'Functionality',
                        'description': 'Design for intended use and performance',
                        'key_considerations': [
                            'User needs',
                            'Ease of use',
                            'Maintenance',
                            'Durability'
                        ]
                    },
                    {
                        'name': 'Aesthetics',
                        'description': 'Design for visual appeal and style',
                        'key_considerations': [
                            'Form',
                            'Color',
                            'Texture',
                            'Proportion'
                        ]
                    },
                    {
                        'name': 'Integration',
                        'description': 'Design for integration with home environment',
                        'key_considerations': [
                            'Space requirements',
                            'Style compatibility',
                            'Existing systems',
                            'Environmental factors'
                        ]
                    }
                ],
                'material_considerations': {
                    'ceramics': {
                        'properties': ['durability', 'heat_resistance', 'water_absorption'],
                        'processing_methods': ['throwing', 'casting', 'firing', 'glazing'],
                        'environmental_impact': ['energy_usage', 'recyclability', 'longevity']
                    },
                    'textiles': {
                        'properties': ['durability', 'texture', 'colorfastness'],
                        'processing_methods': ['weaving', 'printing', 'finishing', 'sewing'],
                        'environmental_impact': ['water_usage', 'chemical_usage', 'biodegradability']
                    },
                    'glass': {
                        'properties': ['transparency', 'strength', 'thermal_resistance'],
                        'processing_methods': ['blowing', 'casting', 'cutting', 'finishing'],
                        'environmental_impact': ['energy_usage', 'recyclability', 'weight']
                    }
                },
                'design_constraints': {
                    'safety_requirements': [
                        'Stability',
                        'Non-toxic materials',
                        'Heat resistance',
                        'Electrical safety'
                    ],
                    'regulatory_requirements': [
                        'Material safety',
                        'Product labeling',
                        'Flammability standards',
                        'Electrical standards'
                    ],
                    'market_considerations': [
                        'Price point',
                        'Target demographic',
                        'Competitive products',
                        'Retail display requirements'
                    ]
                }
            }
        }
        
        # Initialize empty design projects
        self.design_projects = {}
        
        logger.info("Initialized default design database")
    
    def save_database(self, output_path=None):
        """
        Save the design database to a file.
        
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
                    'design_templates': self.design_templates,
                    'industry_configs': self.industry_configs,
                    'design_projects': self.design_projects,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"Saved design database to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving design database: {str(e)}")
            return False
    
    def get_industry_templates(self, industry):
        """
        Get design templates for a specific industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            dict: Design templates for the specified industry
        """
        return self.design_templates.get(industry, {})
    
    def get_template(self, industry, template_id):
        """
        Get a specific design template.
        
        Args:
            industry (str): Industry name
            template_id (str): Template identifier
            
        Returns:
            dict: Design template
        """
        industry_templates = self.get_industry_templates(industry)
        return industry_templates.get(template_id, {})
    
    def get_industry_config(self, industry):
        """
        Get configuration for a specific industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            dict: Industry configuration
        """
        return self.industry_configs.get(industry, {})
    
    def get_design_project(self, project_id):
        """
        Get a specific design project.
        
        Args:
            project_id (str): Project identifier
            
        Returns:
            dict: Design project
        """
        return self.design_projects.get(project_id, {})
    
    def create_design_project(self, name, industry, template_id=None, reference_image=None, description=None):
        """
        Create a new design project.
        
        Args:
            name (str): Project name
            industry (str): Industry name
            template_id (str, optional): Template identifier
            reference_image (str, optional): Path to reference image
            description (str, optional): Project description
            
        Returns:
            str: Project identifier
        """
        try:
            # Generate project ID
            project_id = str(uuid.uuid4())
            
            # Get template if specified
            template = {}
            if template_id:
                template = self.get_template(industry, template_id)
                if not template:
                    logger.warning(f"Template not found: {template_id}")
            
            # Create project
            project = {
                'id': project_id,
                'name': name,
                'industry': industry,
                'description': description or f"Design project for {name}",
                'template_id': template_id,
                'reference_image': reference_image,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'status': 'draft',
                'design_data': {},
                'components': [],
                'materials': [],
                'manufacturing_processes': [],
                'design_parameters': {},
                'analysis_results': {},
                'version_history': []
            }
            
            # Initialize from template if available
            if template:
                # Copy components from template
                project['components'] = []
                for component in template.get('components', []):
                    project['components'].append({
                        'name': component.get('name'),
                        'required': component.get('required', True),
                        'selected_material': None,
                        'properties': component.get('properties', {}),
                        'status': 'pending'
                    })
                
                # Copy design parameters from template
                project['design_parameters'] = {}
                for param_name, param_values in template.get('design_parameters', {}).items():
                    project['design_parameters'][param_name] = {
                        'options': param_values,
                        'selected': None
                    }
                
                # Copy manufacturing processes from template
                project['manufacturing_processes'] = template.get('manufacturing_processes', [])
            
            # Save project
            self.design_projects[project_id] = project
            logger.info(f"Created design project: {project_id}")
            
            return project_id
            
        except Exception as e:
            logger.error(f"Error creating design project: {str(e)}")
            return None
    
    def update_design_project(self, project_id, updates):
        """
        Update a design project.
        
        Args:
            project_id (str): Project identifier
            updates (dict): Project updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return False
            
            # Save current version to history
            current_version = project.copy()
            current_version['version_date'] = project.get('updated_at')
            project.setdefault('version_history', []).append(current_version)
            
            # Update project
            for key, value in updates.items():
                if key not in ['id', 'created_at', 'version_history']:
                    project[key] = value
            
            # Update timestamp
            project['updated_at'] = datetime.now().isoformat()
            
            logger.info(f"Updated design project: {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating design project: {str(e)}")
            return False
    
    def delete_design_project(self, project_id):
        """
        Delete a design project.
        
        Args:
            project_id (str): Project identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if project exists
            if project_id not in self.design_projects:
                logger.error(f"Project not found: {project_id}")
                return False
            
            # Delete project
            del self.design_projects[project_id]
            logger.info(f"Deleted design project: {project_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting design project: {str(e)}")
            return False
    
    def analyze_reference_image(self, project_id, image_path):
        """
        Analyze a reference image for a design project.
        
        Args:
            project_id (str): Project identifier
            image_path (str): Path to reference image
            
        Returns:
            dict: Image analysis results
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return {'error': 'Project not found'}
            
            # Check if image exists
            if not os.path.exists(image_path):
                logger.error(f"Image not found: {image_path}")
                return {'error': 'Image not found'}
            
            # Use image recognition service if available
            if hasattr(self, 'image_recognition_service') and self.image_recognition_service:
                analysis_results = self.image_recognition_service.analyze_image(image_path)
                
                # Update project with reference image and analysis results
                project['reference_image'] = image_path
                project['image_analysis'] = analysis_results
                project['updated_at'] = datetime.now().isoformat()
                
                logger.info(f"Analyzed reference image for project: {project_id}")
                return analysis_results
            else:
                logger.warning("Image recognition service not available")
                return {'error': 'Image recognition service not available'}
            
        except Exception as e:
            logger.error(f"Error analyzing reference image: {str(e)}")
            return {'error': str(e)}
    
    def select_material(self, project_id, component_name, material_id):
        """
        Select a material for a component in a design project.
        
        Args:
            project_id (str): Project identifier
            component_name (str): Component name
            material_id (str): Material identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return False
            
            # Find component
            component = None
            for comp in project.get('components', []):
                if comp.get('name') == component_name:
                    component = comp
                    break
            
            if not component:
                logger.error(f"Component not found: {component_name}")
                return False
            
            # Check if material exists in database
            if hasattr(self, 'material_service') and self.material_service:
                material = self.material_service.get_material(material_id)
                if not material:
                    logger.error(f"Material not found: {material_id}")
                    return False
            
            # Update component with selected material
            component['selected_material'] = material_id
            
            # Add material to project materials list if not already present
            if material_id not in project.get('materials', []):
                project.setdefault('materials', []).append(material_id)
            
            # Update timestamp
            project['updated_at'] = datetime.now().isoformat()
            
            logger.info(f"Selected material {material_id} for component {component_name} in project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error selecting material: {str(e)}")
            return False
    
    def set_design_parameter(self, project_id, parameter_name, parameter_value):
        """
        Set a design parameter for a design project.
        
        Args:
            project_id (str): Project identifier
            parameter_name (str): Parameter name
            parameter_value: Parameter value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return False
            
            # Check if parameter exists
            if parameter_name not in project.get('design_parameters', {}):
                # Create parameter if it doesn't exist
                project.setdefault('design_parameters', {})[parameter_name] = {
                    'options': [],
                    'selected': None
                }
            
            # Update parameter value
            project['design_parameters'][parameter_name]['selected'] = parameter_value
            
            # Update timestamp
            project['updated_at'] = datetime.now().isoformat()
            
            logger.info(f"Set design parameter {parameter_name} to {parameter_value} in project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting design parameter: {str(e)}")
            return False
    
    def analyze_design(self, project_id):
        """
        Analyze a design project for sustainability, trends, and compliance.
        
        Args:
            project_id (str): Project identifier
            
        Returns:
            dict: Design analysis results
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return {'error': 'Project not found'}
            
            # Prepare analysis results
            analysis_results = {
                'timestamp': datetime.now().isoformat(),
                'project_id': project_id,
                'project_name': project.get('name'),
                'industry': project.get('industry')
            }
            
            # Analyze sustainability if service is available
            if hasattr(self, 'sustainability_service') and self.sustainability_service:
                sustainability_analysis = self.sustainability_service.analyze_product_sustainability(project)
                analysis_results['sustainability'] = sustainability_analysis
            
            # Analyze trend alignment if service is available
            if hasattr(self, 'trend_service') and self.trend_service:
                trend_analysis = self.trend_service.analyze_trend_alignment(project)
                analysis_results['trends'] = trend_analysis
            
            # Check compliance if service is available
            if hasattr(self, 'compliance_service') and self.compliance_service:
                compliance_analysis = self.compliance_service.check_product_compliance(project)
                analysis_results['compliance'] = compliance_analysis
            
            # Update project with analysis results
            project['analysis_results'] = analysis_results
            project['updated_at'] = datetime.now().isoformat()
            
            logger.info(f"Analyzed design for project: {project_id}")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing design: {str(e)}")
            return {'error': str(e)}
    
    def generate_design_recommendations(self, project_id):
        """
        Generate design recommendations for a project based on analysis results.
        
        Args:
            project_id (str): Project identifier
            
        Returns:
            dict: Design recommendations
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return {'error': 'Project not found'}
            
            # Check if analysis results exist
            analysis_results = project.get('analysis_results', {})
            if not analysis_results:
                # Perform analysis if not already done
                analysis_results = self.analyze_design(project_id)
            
            # Generate recommendations
            recommendations = {
                'timestamp': datetime.now().isoformat(),
                'project_id': project_id,
                'project_name': project.get('name'),
                'industry': project.get('industry'),
                'categories': {}
            }
            
            # Material recommendations
            material_recommendations = self._generate_material_recommendations(project, analysis_results)
            if material_recommendations:
                recommendations['categories']['materials'] = material_recommendations
            
            # Design parameter recommendations
            parameter_recommendations = self._generate_parameter_recommendations(project, analysis_results)
            if parameter_recommendations:
                recommendations['categories']['design_parameters'] = parameter_recommendations
            
            # Manufacturing process recommendations
            process_recommendations = self._generate_process_recommendations(project, analysis_results)
            if process_recommendations:
                recommendations['categories']['manufacturing_processes'] = process_recommendations
            
            # Sustainability recommendations
            sustainability_recommendations = self._extract_sustainability_recommendations(analysis_results)
            if sustainability_recommendations:
                recommendations['categories']['sustainability'] = sustainability_recommendations
            
            # Trend recommendations
            trend_recommendations = self._extract_trend_recommendations(analysis_results)
            if trend_recommendations:
                recommendations['categories']['trends'] = trend_recommendations
            
            # Compliance recommendations
            compliance_recommendations = self._extract_compliance_recommendations(analysis_results)
            if compliance_recommendations:
                recommendations['categories']['compliance'] = compliance_recommendations
            
            # Update project with recommendations
            project['design_recommendations'] = recommendations
            project['updated_at'] = datetime.now().isoformat()
            
            logger.info(f"Generated design recommendations for project: {project_id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating design recommendations: {str(e)}")
            return {'error': str(e)}
    
    def _generate_material_recommendations(self, project, analysis_results):
        """
        Generate material recommendations based on analysis results.
        
        Args:
            project (dict): Project data
            analysis_results (dict): Analysis results
            
        Returns:
            list: Material recommendations
        """
        recommendations = []
        
        # Get sustainability analysis
        sustainability = analysis_results.get('sustainability', {})
        
        # Check component analyses
        component_analyses = sustainability.get('component_analyses', [])
        for component_analysis in component_analyses:
            material_analysis = component_analysis.get('material_analysis', {})
            
            # Check if material has weaknesses
            if material_analysis and material_analysis.get('weaknesses'):
                component_name = component_analysis.get('name', 'Component')
                current_material = component_analysis.get('material')
                
                # Find alternative materials
                alternative_materials = []
                if hasattr(self, 'material_service') and self.material_service:
                    # Get material properties to match
                    material_properties = {}
                    for comp in project.get('components', []):
                        if comp.get('name') == component_name:
                            material_properties = comp.get('properties', {})
                            break
                    
                    # Find alternatives with better sustainability
                    alternative_materials = self.material_service.find_alternative_materials(
                        current_material, 
                        material_properties,
                        sustainability_focus=True
                    )
                
                # Create recommendation
                if alternative_materials:
                    recommendations.append({
                        'component': component_name,
                        'current_material': current_material,
                        'issues': material_analysis.get('weaknesses', []),
                        'alternatives': alternative_materials,
                        'priority': 'High' if material_analysis.get('sustainability_score', 0) < 40 else 'Medium'
                    })
        
        return recommendations
    
    def _generate_parameter_recommendations(self, project, analysis_results):
        """
        Generate design parameter recommendations based on analysis results.
        
        Args:
            project (dict): Project data
            analysis_results (dict): Analysis results
            
        Returns:
            list: Design parameter recommendations
        """
        recommendations = []
        
        # Get trend analysis
        trends = analysis_results.get('trends', {})
        
        # Check trend alignments
        global_alignments = trends.get('global_trend_alignments', [])
        industry_alignments = trends.get('industry_trend_alignments', [])
        
        # Find low alignment trends
        low_alignment_trends = []
        for alignment in global_alignments + industry_alignments:
            if alignment.get('score', 1) < 0.3:  # Less than 30% alignment
                low_alignment_trends.append(alignment)
        
        # Generate recommendations for design parameters
        for trend_alignment in low_alignment_trends:
            trend_name = trend_alignment.get('trend', '')
            missing_elements = trend_alignment.get('missing_elements', [])
            
            # Map trend elements to design parameters
            parameter_recommendations = []
            for element in missing_elements:
                # Simple mapping based on element keywords
                element_lower = element.lower()
                
                if 'sustainable' in element_lower or 'eco' in element_lower:
                    parameter_recommendations.append({
                        'parameter': 'sustainability_level',
                        'value': 'eco-friendly'
                    })
                
                elif 'modular' in element_lower or 'adaptable' in element_lower:
                    parameter_recommendations.append({
                        'parameter': 'modularity',
                        'value': 'high'
                    })
                
                elif 'minimal' in element_lower or 'simple' in element_lower:
                    parameter_recommendations.append({
                        'parameter': 'style',
                        'value': 'minimalist'
                    })
                
                elif 'smart' in element_lower or 'connected' in element_lower:
                    parameter_recommendations.append({
                        'parameter': 'technology_integration',
                        'value': 'smart'
                    })
            
            # Add recommendation if parameters found
            if parameter_recommendations:
                recommendations.append({
                    'trend': trend_name,
                    'alignment_score': f"{int(trend_alignment.get('score', 0) * 100)}%",
                    'missing_elements': missing_elements,
                    'parameter_changes': parameter_recommendations,
                    'priority': 'Medium'
                })
        
        return recommendations
    
    def _generate_process_recommendations(self, project, analysis_results):
        """
        Generate manufacturing process recommendations based on analysis results.
        
        Args:
            project (dict): Project data
            analysis_results (dict): Analysis results
            
        Returns:
            list: Manufacturing process recommendations
        """
        recommendations = []
        
        # Get sustainability analysis
        sustainability = analysis_results.get('sustainability', {})
        
        # Check component analyses
        component_analyses = sustainability.get('component_analyses', [])
        for component_analysis in component_analyses:
            process_analysis = component_analysis.get('process_analysis', {})
            
            # Check if process has weaknesses
            if process_analysis and process_analysis.get('weaknesses'):
                component_name = component_analysis.get('name', 'Component')
                current_process = component_analysis.get('process')
                
                # Find alternative processes
                alternative_processes = []
                if hasattr(self, 'material_service') and self.material_service:
                    # Get material for the component
                    component_material = None
                    for comp in project.get('components', []):
                        if comp.get('name') == component_name:
                            component_material = comp.get('selected_material')
                            break
                    
                    # Find alternatives with better sustainability
                    if component_material:
                        alternative_processes = self.material_service.find_alternative_processes(
                            component_material,
                            current_process,
                            sustainability_focus=True
                        )
                
                # Create recommendation
                if alternative_processes:
                    recommendations.append({
                        'component': component_name,
                        'current_process': current_process,
                        'issues': process_analysis.get('weaknesses', []),
                        'alternatives': alternative_processes,
                        'priority': 'Medium'
                    })
        
        return recommendations
    
    def _extract_sustainability_recommendations(self, analysis_results):
        """
        Extract sustainability recommendations from analysis results.
        
        Args:
            analysis_results (dict): Analysis results
            
        Returns:
            list: Sustainability recommendations
        """
        sustainability = analysis_results.get('sustainability', {})
        return sustainability.get('recommendations', [])
    
    def _extract_trend_recommendations(self, analysis_results):
        """
        Extract trend recommendations from analysis results.
        
        Args:
            analysis_results (dict): Analysis results
            
        Returns:
            list: Trend recommendations
        """
        trends = analysis_results.get('trends', {})
        return trends.get('recommendations', [])
    
    def _extract_compliance_recommendations(self, analysis_results):
        """
        Extract compliance recommendations from analysis results.
        
        Args:
            analysis_results (dict): Analysis results
            
        Returns:
            list: Compliance recommendations
        """
        compliance = analysis_results.get('compliance', {})
        return compliance.get('recommendations', [])
    
    def generate_design_visualization(self, project_id):
        """
        Generate visualization data for a design project.
        
        Args:
            project_id (str): Project identifier
            
        Returns:
            dict: Visualization data
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return {'error': 'Project not found'}
            
            # Generate visualization data
            visualization = {
                'project_id': project_id,
                'project_name': project.get('name'),
                'industry': project.get('industry'),
                'components': [],
                'materials': [],
                'parameters': {},
                'analysis_summary': {}
            }
            
            # Add components
            for component in project.get('components', []):
                component_data = {
                    'name': component.get('name'),
                    'material': component.get('selected_material'),
                    'properties': component.get('properties', {})
                }
                visualization['components'].append(component_data)
            
            # Add materials
            for material_id in project.get('materials', []):
                material_data = {'id': material_id}
                
                # Get material details if service is available
                if hasattr(self, 'material_service') and self.material_service:
                    material = self.material_service.get_material(material_id)
                    if material:
                        material_data.update({
                            'name': material.get('name'),
                            'category': material.get('category'),
                            'properties': material.get('properties', {})
                        })
                
                visualization['materials'].append(material_data)
            
            # Add design parameters
            for param_name, param_data in project.get('design_parameters', {}).items():
                visualization['parameters'][param_name] = param_data.get('selected')
            
            # Add analysis summary
            analysis_results = project.get('analysis_results', {})
            
            # Sustainability summary
            sustainability = analysis_results.get('sustainability', {})
            if sustainability:
                visualization['analysis_summary']['sustainability'] = {
                    'score': sustainability.get('sustainability_score', 0),
                    'level': sustainability.get('sustainability_level', 'Unknown')
                }
            
            # Trend alignment summary
            trends = analysis_results.get('trends', {})
            if trends:
                visualization['analysis_summary']['trend_alignment'] = {
                    'score': trends.get('overall_alignment', 0),
                    'level': trends.get('alignment_level', 'Unknown')
                }
            
            # Compliance summary
            compliance = analysis_results.get('compliance', {})
            if compliance:
                visualization['analysis_summary']['compliance'] = {
                    'status': compliance.get('compliance_status', 'Unknown'),
                    'issues': {
                        'critical': compliance.get('critical_issues', 0),
                        'high': compliance.get('high_issues', 0),
                        'medium': compliance.get('medium_issues', 0)
                    }
                }
            
            logger.info(f"Generated design visualization for project: {project_id}")
            return visualization
            
        except Exception as e:
            logger.error(f"Error generating design visualization: {str(e)}")
            return {'error': str(e)}
    
    def export_design_data(self, project_id, format='json'):
        """
        Export design data for a project.
        
        Args:
            project_id (str): Project identifier
            format (str): Export format ('json', 'csv', 'pdf')
            
        Returns:
            dict: Export data and metadata
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return {'error': 'Project not found'}
            
            # Prepare export data
            export_data = {
                'metadata': {
                    'project_id': project_id,
                    'project_name': project.get('name'),
                    'industry': project.get('industry'),
                    'created_at': project.get('created_at'),
                    'updated_at': project.get('updated_at'),
                    'export_date': datetime.now().isoformat(),
                    'format': format
                }
            }
            
            # Export based on format
            if format == 'json':
                # Full JSON export
                export_data['content'] = project
                export_data['file_extension'] = 'json'
            
            elif format == 'csv':
                # CSV export (simplified)
                csv_data = []
                
                # Add components
                for component in project.get('components', []):
                    csv_data.append({
                        'type': 'component',
                        'name': component.get('name'),
                        'material': component.get('selected_material'),
                        'required': component.get('required', True)
                    })
                
                # Add design parameters
                for param_name, param_data in project.get('design_parameters', {}).items():
                    csv_data.append({
                        'type': 'parameter',
                        'name': param_name,
                        'value': param_data.get('selected')
                    })
                
                export_data['content'] = csv_data
                export_data['file_extension'] = 'csv'
            
            elif format == 'pdf':
                # PDF export (metadata only, actual PDF generation would be handled separately)
                export_data['content'] = {
                    'project_summary': {
                        'name': project.get('name'),
                        'industry': project.get('industry'),
                        'description': project.get('description'),
                        'status': project.get('status')
                    },
                    'components': project.get('components', []),
                    'design_parameters': project.get('design_parameters', {}),
                    'analysis_results': project.get('analysis_results', {})
                }
                export_data['file_extension'] = 'pdf'
            
            else:
                logger.error(f"Unsupported export format: {format}")
                return {'error': f"Unsupported export format: {format}"}
            
            logger.info(f"Exported design data for project: {project_id} in {format} format")
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting design data: {str(e)}")
            return {'error': str(e)}
    
    def process_design_command(self, project_id, command_data):
        """
        Process a design command for a project.
        
        Args:
            project_id (str): Project identifier
            command_data (dict): Command data from NLP processing
            
        Returns:
            dict: Command result
        """
        try:
            # Get project
            project = self.get_design_project(project_id)
            if not project:
                logger.error(f"Project not found: {project_id}")
                return {'error': 'Project not found', 'success': False}
            
            # Extract command information
            command_type = command_data.get('intent', {}).get('type')
            entities = command_data.get('entities', {})
            
            # Process command based on type
            result = {
                'success': False,
                'message': '',
                'data': {}
            }
            
            if command_type == 'select_material':
                # Extract component and material
                component_name = entities.get('component')
                material_name = entities.get('material')
                
                if not component_name or not material_name:
                    result['message'] = 'Missing component or material information'
                    return result
                
                # Find material ID from name
                material_id = None
                if hasattr(self, 'material_service') and self.material_service:
                    material = self.material_service.find_material_by_name(material_name)
                    if material:
                        material_id = material.get('id')
                
                if not material_id:
                    result['message'] = f"Material not found: {material_name}"
                    return result
                
                # Select material
                success = self.select_material(project_id, component_name, material_id)
                
                if success:
                    result['success'] = True
                    result['message'] = f"Selected {material_name} for {component_name}"
                    result['data'] = {'component': component_name, 'material': material_id}
                else:
                    result['message'] = f"Failed to select material"
            
            elif command_type == 'set_parameter':
                # Extract parameter and value
                parameter_name = entities.get('parameter')
                parameter_value = entities.get('value')
                
                if not parameter_name or parameter_value is None:
                    result['message'] = 'Missing parameter or value information'
                    return result
                
                # Set parameter
                success = self.set_design_parameter(project_id, parameter_name, parameter_value)
                
                if success:
                    result['success'] = True
                    result['message'] = f"Set {parameter_name} to {parameter_value}"
                    result['data'] = {'parameter': parameter_name, 'value': parameter_value}
                else:
                    result['message'] = f"Failed to set parameter"
            
            elif command_type == 'analyze_design':
                # Analyze design
                analysis_results = self.analyze_design(project_id)
                
                if 'error' not in analysis_results:
                    result['success'] = True
                    result['message'] = f"Design analysis completed"
                    result['data'] = {'analysis_summary': {
                        'sustainability': analysis_results.get('sustainability', {}).get('sustainability_level', 'Unknown'),
                        'trend_alignment': analysis_results.get('trends', {}).get('alignment_level', 'Unknown'),
                        'compliance': analysis_results.get('compliance', {}).get('compliance_status', 'Unknown')
                    }}
                else:
                    result['message'] = f"Failed to analyze design: {analysis_results.get('error')}"
            
            elif command_type == 'get_recommendations':
                # Generate recommendations
                recommendations = self.generate_design_recommendations(project_id)
                
                if 'error' not in recommendations:
                    result['success'] = True
                    result['message'] = f"Design recommendations generated"
                    result['data'] = {'recommendation_count': sum(len(recs) for recs in recommendations.get('categories', {}).values())}
                else:
                    result['message'] = f"Failed to generate recommendations: {recommendations.get('error')}"
            
            else:
                result['message'] = f"Unsupported command type: {command_type}"
            
            logger.info(f"Processed design command for project {project_id}: {command_type}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing design command: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def create_design_template(self, industry, template_id, template_data):
        """
        Create a new design template.
        
        Args:
            industry (str): Industry name
            template_id (str): Template identifier
            template_data (dict): Template information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate template data
            required_fields = ['name', 'description', 'components']
            for field in required_fields:
                if field not in template_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Create industry category if it doesn't exist
            if industry not in self.design_templates:
                self.design_templates[industry] = {}
            
            # Add template
            self.design_templates[industry][template_id] = template_data
            logger.info(f"Created design template: {template_id} for {industry}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating design template: {str(e)}")
            return False
    
    def update_design_template(self, industry, template_id, template_updates):
        """
        Update an existing design template.
        
        Args:
            industry (str): Industry name
            template_id (str): Template identifier
            template_updates (dict): Template updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if template exists
            if industry not in self.design_templates or template_id not in self.design_templates[industry]:
                logger.error(f"Template not found: {industry}/{template_id}")
                return False
            
            # Update template
            for key, value in template_updates.items():
                self.design_templates[industry][template_id][key] = value
            
            logger.info(f"Updated design template: {template_id} for {industry}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating design template: {str(e)}")
            return False
    
    def delete_design_template(self, industry, template_id):
        """
        Delete a design template.
        
        Args:
            industry (str): Industry name
            template_id (str): Template identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if template exists
            if industry not in self.design_templates or template_id not in self.design_templates[industry]:
                logger.error(f"Template not found: {industry}/{template_id}")
                return False
            
            # Delete template
            del self.design_templates[industry][template_id]
            logger.info(f"Deleted design template: {template_id} for {industry}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting design template: {str(e)}")
            return False


if __name__ == "__main__":
    # Example usage
    manager = DesignManager()
    
    # Get templates for an industry
    furniture_templates = manager.get_industry_templates('furniture')
    print(f"Found {len(furniture_templates)} furniture templates")
    
    # Create a design project
    project_id = manager.create_design_project(
        name="Modern Office Chair",
        industry="furniture",
        template_id="chair",
        description="Ergonomic office chair with sustainable materials"
    )
    
    if project_id:
        print(f"Created design project: {project_id}")
        
        # Select materials for components
        manager.select_material(project_id, "Seat", "recycled_plastic")
        manager.select_material(project_id, "Backrest", "recycled_plastic")
        manager.select_material(project_id, "Legs/Base", "aluminum")
        
        # Set design parameters
        manager.set_design_parameter(project_id, "style", "modern")
        manager.set_design_parameter(project_id, "use_case", "office")
        manager.set_design_parameter(project_id, "sustainability_level", "eco-friendly")
        
        # Analyze design
        analysis_results = manager.analyze_design(project_id)
        print(f"Design analysis completed")
        
        # Generate recommendations
        recommendations = manager.generate_design_recommendations(project_id)
        print(f"Generated design recommendations")
        
        # Generate visualization
        visualization = manager.generate_design_visualization(project_id)
        print(f"Generated design visualization")
        
        # Export design data
        export_data = manager.export_design_data(project_id, format='json')
        print(f"Exported design data")
