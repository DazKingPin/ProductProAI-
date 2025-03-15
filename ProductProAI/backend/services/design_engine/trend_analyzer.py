import logging
import json
import os
import random
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrendAnalyzer:
    """
    Class for analyzing market trends and consumer preferences in product design.
    Provides trend-based design recommendations aligned with current and future market demands.
    """
    
    def __init__(self, database_path=None):
        """
        Initialize the TrendAnalyzer.
        
        Args:
            database_path (str, optional): Path to the trends database file
        """
        logger.info("Initializing TrendAnalyzer")
        self.database_path = database_path
        self.trends = {}
        self.industry_trends = {}
        self.consumer_preferences = {}
        self.trend_forecasts = {}
        self._load_trend_data()
    
    def _load_trend_data(self):
        """
        Load trend data from database file or initialize with default data.
        """
        try:
            if self.database_path and os.path.exists(self.database_path):
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    self.trends = data.get('trends', {})
                    self.industry_trends = data.get('industry_trends', {})
                    self.consumer_preferences = data.get('consumer_preferences', {})
                    self.trend_forecasts = data.get('trend_forecasts', {})
                logger.info(f"Loaded trend data from database")
            else:
                logger.info("Initializing default trend database")
                self._initialize_default_data()
        except Exception as e:
            logger.error(f"Error loading trend data: {str(e)}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """
        Initialize the database with default trend data.
        """
        # Initialize global design trends
        self.trends = {
            'sustainability': {
                'name': 'Sustainability',
                'description': 'Eco-friendly design approaches and materials',
                'strength': 0.9,  # 0-1 scale
                'growth_rate': 0.15,  # annual growth rate
                'maturity': 'Growing',  # Emerging, Growing, Mature, Declining
                'key_elements': [
                    'Recycled materials',
                    'Energy efficiency',
                    'Circular design',
                    'Waste reduction',
                    'Biodegradable materials'
                ],
                'examples': [
                    'Furniture made from ocean plastic',
                    'Carbon-negative packaging',
                    'Modular designs for easy repair',
                    'Products with environmental impact labels'
                ]
            },
            'minimalism': {
                'name': 'Minimalism',
                'description': 'Clean, simple designs with essential elements only',
                'strength': 0.8,
                'growth_rate': 0.05,
                'maturity': 'Mature',
                'key_elements': [
                    'Clean lines',
                    'Neutral colors',
                    'Functional focus',
                    'Reduced ornamentation',
                    'Quality over quantity'
                ],
                'examples': [
                    'Scandinavian furniture',
                    'Monochromatic color schemes',
                    'Simplified user interfaces',
                    'Streamlined packaging'
                ]
            },
            'biophilic_design': {
                'name': 'Biophilic Design',
                'description': 'Incorporating nature and natural elements into design',
                'strength': 0.75,
                'growth_rate': 0.2,
                'maturity': 'Growing',
                'key_elements': [
                    'Natural materials',
                    'Organic shapes',
                    'Living elements',
                    'Natural light',
                    'Nature-inspired patterns'
                ],
                'examples': [
                    'Wood and stone furniture',
                    'Plant-integrated products',
                    'Nature-inspired textures',
                    'Products with living components'
                ]
            },
            'smart_integration': {
                'name': 'Smart Integration',
                'description': 'Embedding technology seamlessly into products',
                'strength': 0.85,
                'growth_rate': 0.25,
                'maturity': 'Growing',
                'key_elements': [
                    'IoT connectivity',
                    'Invisible technology',
                    'Voice control',
                    'App integration',
                    'Adaptive functionality'
                ],
                'examples': [
                    'Smart furniture with charging capabilities',
                    'Connected home products',
                    'Voice-activated devices',
                    'Self-adjusting products'
                ]
            },
            'customization': {
                'name': 'Customization',
                'description': 'Personalized products tailored to individual preferences',
                'strength': 0.7,
                'growth_rate': 0.18,
                'maturity': 'Growing',
                'key_elements': [
                    'Modular components',
                    'User-adjustable features',
                    'Personalization options',
                    'Made-to-order manufacturing',
                    'Co-creation platforms'
                ],
                'examples': [
                    'Modular furniture systems',
                    'Customizable color schemes',
                    'User-assembled products',
                    'Personalized packaging'
                ]
            },
            'nostalgic_design': {
                'name': 'Nostalgic Design',
                'description': 'Designs that evoke past eras with modern updates',
                'strength': 0.65,
                'growth_rate': 0.1,
                'maturity': 'Growing',
                'key_elements': [
                    'Retro aesthetics',
                    'Vintage materials',
                    'Historical references',
                    'Traditional craftsmanship',
                    'Modern functionality'
                ],
                'examples': [
                    'Mid-century modern furniture revivals',
                    'Vintage-inspired electronics',
                    'Traditional patterns with contemporary colors',
                    'Analog-digital hybrid products'
                ]
            },
            'multifunctionality': {
                'name': 'Multifunctionality',
                'description': 'Products that serve multiple purposes',
                'strength': 0.8,
                'growth_rate': 0.15,
                'maturity': 'Growing',
                'key_elements': [
                    'Space-saving design',
                    'Convertible features',
                    'Adaptable functionality',
                    'Integrated solutions',
                    'Versatile use cases'
                ],
                'examples': [
                    'Sofa beds and convertible furniture',
                    'Modular storage systems',
                    'Multi-tool products',
                    'Transformable designs'
                ]
            },
            'inclusive_design': {
                'name': 'Inclusive Design',
                'description': 'Designs accessible to people of all abilities and backgrounds',
                'strength': 0.7,
                'growth_rate': 0.22,
                'maturity': 'Growing',
                'key_elements': [
                    'Universal accessibility',
                    'Adaptable interfaces',
                    'Ergonomic considerations',
                    'Cultural sensitivity',
                    'Age-friendly features'
                ],
                'examples': [
                    'Easy-grip utensils',
                    'Adjustable-height furniture',
                    'High-contrast interfaces',
                    'Multilingual packaging'
                ]
            }
        }
        
        # Initialize industry-specific trends
        self.industry_trends = {
            'furniture': {
                'modular_systems': {
                    'name': 'Modular Systems',
                    'description': 'Furniture that can be reconfigured and adapted to different spaces',
                    'strength': 0.85,
                    'growth_rate': 0.2,
                    'key_elements': [
                        'Interchangeable components',
                        'Flexible configurations',
                        'Easy assembly/disassembly',
                        'Scalable designs'
                    ]
                },
                'multifunctional_furniture': {
                    'name': 'Multifunctional Furniture',
                    'description': 'Pieces that serve multiple purposes to maximize space efficiency',
                    'strength': 0.8,
                    'growth_rate': 0.15,
                    'key_elements': [
                        'Storage integration',
                        'Convertible features',
                        'Space-saving design',
                        'Adaptable functionality'
                    ]
                },
                'sustainable_materials': {
                    'name': 'Sustainable Materials',
                    'description': 'Use of eco-friendly and responsibly sourced materials',
                    'strength': 0.9,
                    'growth_rate': 0.25,
                    'key_elements': [
                        'Reclaimed wood',
                        'Recycled plastics',
                        'Biodegradable materials',
                        'Low-impact finishes'
                    ]
                }
            },
            'electronics': {
                'seamless_integration': {
                    'name': 'Seamless Integration',
                    'description': 'Technology that blends invisibly into environments',
                    'strength': 0.85,
                    'growth_rate': 0.2,
                    'key_elements': [
                        'Hidden technology',
                        'Ambient computing',
                        'Wireless connectivity',
                        'Intuitive interfaces'
                    ]
                },
                'sustainable_electronics': {
                    'name': 'Sustainable Electronics',
                    'description': 'Devices designed with environmental impact in mind',
                    'strength': 0.75,
                    'growth_rate': 0.3,
                    'key_elements': [
                        'Energy efficiency',
                        'Recyclable components',
                        'Modular design for repair',
                        'Extended product lifespan'
                    ]
                },
                'adaptive_interfaces': {
                    'name': 'Adaptive Interfaces',
                    'description': 'Interfaces that adjust to user preferences and behaviors',
                    'strength': 0.8,
                    'growth_rate': 0.25,
                    'key_elements': [
                        'AI personalization',
                        'Context awareness',
                        'Multimodal interaction',
                        'Accessibility features'
                    ]
                }
            },
            'packaging': {
                'plastic_alternatives': {
                    'name': 'Plastic Alternatives',
                    'description': 'Sustainable alternatives to conventional plastic packaging',
                    'strength': 0.9,
                    'growth_rate': 0.35,
                    'key_elements': [
                        'Biodegradable materials',
                        'Plant-based plastics',
                        'Paper and cardboard innovations',
                        'Edible packaging'
                    ]
                },
                'minimalist_packaging': {
                    'name': 'Minimalist Packaging',
                    'description': 'Reduced packaging that maintains functionality with less material',
                    'strength': 0.85,
                    'growth_rate': 0.2,
                    'key_elements': [
                        'Material reduction',
                        'Structural optimization',
                        'Elimination of unnecessary elements',
                        'Concentrated products'
                    ]
                },
                'reusable_systems': {
                    'name': 'Reusable Systems',
                    'description': 'Packaging designed for multiple uses rather than single-use',
                    'strength': 0.8,
                    'growth_rate': 0.3,
                    'key_elements': [
                        'Refill systems',
                        'Returnable packaging',
                        'Durable materials',
                        'Multi-purpose design'
                    ]
                }
            },
            'fashion': {
                'sustainable_fashion': {
                    'name': 'Sustainable Fashion',
                    'description': 'Clothing and accessories with reduced environmental impact',
                    'strength': 0.9,
                    'growth_rate': 0.3,
                    'key_elements': [
                        'Organic materials',
                        'Recycled fabrics',
                        'Ethical production',
                        'Circular business models'
                    ]
                },
                'adaptable_clothing': {
                    'name': 'Adaptable Clothing',
                    'description': 'Garments that can be styled or worn in multiple ways',
                    'strength': 0.7,
                    'growth_rate': 0.2,
                    'key_elements': [
                        'Convertible designs',
                        'Modular components',
                        'Adjustable features',
                        'Season-spanning styles'
                    ]
                },
                'tech_integration': {
                    'name': 'Tech Integration',
                    'description': 'Incorporation of technology into clothing and accessories',
                    'strength': 0.75,
                    'growth_rate': 0.25,
                    'key_elements': [
                        'Smart fabrics',
                        'Wearable technology',
                        'Connected accessories',
                        'Functional enhancements'
                    ]
                }
            },
            'home_goods': {
                'smart_home_integration': {
                    'name': 'Smart Home Integration',
                    'description': 'Home products that connect to smart home ecosystems',
                    'strength': 0.85,
                    'growth_rate': 0.25,
                    'key_elements': [
                        'IoT connectivity',
                        'Voice control',
                        'Automation features',
                        'App integration'
                    ]
                },
                'biophilic_elements': {
                    'name': 'Biophilic Elements',
                    'description': 'Products that incorporate or mimic natural elements',
                    'strength': 0.8,
                    'growth_rate': 0.2,
                    'key_elements': [
                        'Natural materials',
                        'Plant integration',
                        'Organic shapes',
                        'Nature-inspired patterns'
                    ]
                },
                'wellness_focus': {
                    'name': 'Wellness Focus',
                    'description': 'Products designed to enhance physical and mental wellbeing',
                    'strength': 0.75,
                    'growth_rate': 0.3,
                    'key_elements': [
                        'Air purification',
                        'Ergonomic design',
                        'Stress reduction features',
                        'Health monitoring integration'
                    ]
                }
            }
        }
        
        # Initialize consumer preferences
        self.consumer_preferences = {
            'sustainability': {
                'importance': 0.85,  # 0-1 scale
                'growth_rate': 0.2,  # annual growth rate
                'demographic_variations': {
                    'gen_z': 0.9,
                    'millennials': 0.85,
                    'gen_x': 0.7,
                    'boomers': 0.6
                },
                'regional_variations': {
                    'north_america': 0.8,
                    'europe': 0.9,
                    'asia': 0.75,
                    'australia': 0.85,
                    'south_america': 0.7,
                    'africa': 0.65
                },
                'key_factors': [
                    'Environmental impact',
                    'Ethical production',
                    'Material sourcing',
                    'End-of-life considerations'
                ]
            },
            'functionality': {
                'importance': 0.9,
                'growth_rate': 0.05,
                'demographic_variations': {
                    'gen_z': 0.85,
                    'millennials': 0.9,
                    'gen_x': 0.9,
                    'boomers': 0.85
                },
                'regional_variations': {
                    'north_america': 0.9,
                    'europe': 0.85,
                    'asia': 0.9,
                    'australia': 0.85,
                    'south_america': 0.8,
                    'africa': 0.85
                },
                'key_factors': [
                    'Ease of use',
                    'Problem-solving capability',
                    'Versatility',
                    'Performance reliability'
                ]
            },
            'aesthetics': {
                'importance': 0.8,
                'growth_rate': 0.1,
                'demographic_variations': {
                    'gen_z': 0.85,
                    'millennials': 0.85,
                    'gen_x': 0.8,
                    'boomers': 0.75
                },
                'regional_variations': {
                    'north_america': 0.8,
                    'europe': 0.85,
                    'asia': 0.9,
                    'australia': 0.8,
                    'south_america': 0.85,
                    'africa': 0.8
                },
                'key_factors': [
                    'Visual appeal',
                    'Style alignment',
                    'Color preferences',
                    'Material appearance'
                ]
            },
            'customization': {
                'importance': 0.7,
                'growth_rate': 0.15,
                'demographic_variations': {
                    'gen_z': 0.85,
                    'millennials': 0.8,
                    'gen_x': 0.7,
                    'boomers': 0.5
                },
                'regional_variations': {
                    'north_america': 0.75,
                    'europe': 0.7,
                    'asia': 0.8,
                    'australia': 0.7,
                    'south_america': 0.65,
                    'africa': 0.6
                },
                'key_factors': [
                    'Personalization options',
                    'Adaptability to preferences',
                    'Co-creation opportunities',
                    'Unique identity'
                ]
            },
            'technology_integration': {
                'importance': 0.75,
                'growth_rate': 0.2,
                'demographic_variations': {
                    'gen_z': 0.9,
                    'millennials': 0.85,
                    'gen_x': 0.7,
                    'boomers': 0.5
                },
                'regional_variations': {
                    'north_america': 0.8,
                    'europe': 0.75,
                    'asia': 0.9,
                    'australia': 0.75,
                    'south_america': 0.7,
                    'africa': 0.65
                },
                'key_factors': [
                    'Connectivity features',
                    'Smart functionality',
                    'Digital enhancement',
                    'Technological innovation'
                ]
            },
            'durability': {
                'importance': 0.85,
                'growth_rate': 0.1,
                'demographic_variations': {
                    'gen_z': 0.8,
                    'millennials': 0.85,
                    'gen_x': 0.9,
                    'boomers': 0.9
                },
                'regional_variations': {
                    'north_america': 0.85,
                    'europe': 0.9,
                    'asia': 0.8,
                    'australia': 0.85,
                    'south_america': 0.9,
                    'africa': 0.9
                },
                'key_factors': [
                    'Product lifespan',
                    'Quality of materials',
                    'Resistance to wear',
                    'Repairability'
                ]
            },
            'price_value': {
                'importance': 0.9,
                'growth_rate': 0.05,
                'demographic_variations': {
                    'gen_z': 0.9,
                    'millennials': 0.85,
                    'gen_x': 0.8,
                    'boomers': 0.85
                },
                'regional_variations': {
                    'north_america': 0.85,
                    'europe': 0.8,
                    'asia': 0.9,
                    'australia': 0.8,
                    'south_america': 0.95,
                    'africa': 0.95
                },
                'key_factors': [
                    'Cost effectiveness',
                    'Perceived value',
                    'Price-to-quality ratio',
                    'Long-term value'
                ]
            }
        }
        
        # Initialize trend forecasts
        self.trend_forecasts = {
            'emerging_trends': [
                {
                    'name': 'Regenerative Design',
                    'description': 'Products that actively restore or regenerate environmental systems',
                    'probability': 0.8,  # 0-1 scale
                    'estimated_timeline': '2-3 years',
                    'potential_impact': 'High',
                    'key_indicators': [
                        'Carbon-negative materials',
                        'Ecosystem restoration focus',
                        'Regenerative business models',
                        'Beyond sustainability mindset'
                    ]
                },
                {
                    'name': 'Hyper-Personalization',
                    'description': 'AI-driven personalization of products based on individual data',
                    'probability': 0.75,
                    'estimated_timeline': '1-2 years',
                    'potential_impact': 'High',
                    'key_indicators': [
                        'AI customization platforms',
                        'Personal data integration',
                        'Real-time adaptation',
                        'Mass customization technologies'
                    ]
                },
                {
                    'name': 'Digital-Physical Hybrids',
                    'description': 'Products that blend digital experiences with physical objects',
                    'probability': 0.85,
                    'estimated_timeline': '1-3 years',
                    'potential_impact': 'High',
                    'key_indicators': [
                        'Augmented reality integration',
                        'Physical products with digital twins',
                        'Interactive physical objects',
                        'Metaverse-compatible products'
                    ]
                },
                {
                    'name': 'Emotional Design',
                    'description': 'Products designed to create specific emotional responses',
                    'probability': 0.7,
                    'estimated_timeline': '2-4 years',
                    'potential_impact': 'Medium',
                    'key_indicators': [
                        'Sensory engagement features',
                        'Mood-enhancing properties',
                        'Emotional intelligence in products',
                        'Psychological well-being focus'
                    ]
                },
                {
                    'name': 'Biomimicry 2.0',
                    'description': 'Advanced application of nature-inspired solutions to design challenges',
                    'probability': 0.65,
                    'estimated_timeline': '3-5 years',
                    'potential_impact': 'High',
                    'key_indicators': [
                        'Self-healing materials',
                        'Adaptive structures',
                        'Energy-efficient natural systems',
                        'Biological integration'
                    ]
                }
            ],
            'declining_trends': [
                {
                    'name': 'Single-Use Products',
                    'description': 'Products designed for one-time use and disposal',
                    'decline_rate': 0.15,  # annual decline rate
                    'estimated_timeline': '3-5 years',
                    'key_indicators': [
                        'Regulatory restrictions',
                        'Consumer rejection',
                        'Reusable alternatives growth',
                        'Corporate sustainability commitments'
                    ]
                },
                {
                    'name': 'Planned Obsolescence',
                    'description': 'Designing products to fail or become outdated quickly',
                    'decline_rate': 0.1,
                    'estimated_timeline': '5-7 years',
                    'key_indicators': [
                        'Right-to-repair legislation',
                        'Durability as selling point',
                        'Consumer backlash',
                        'Circular economy adoption'
                    ]
                },
                {
                    'name': 'Over-Complicated Interfaces',
                    'description': 'Complex user interfaces with steep learning curves',
                    'decline_rate': 0.2,
                    'estimated_timeline': '2-4 years',
                    'key_indicators': [
                        'Minimalist UI/UX preference',
                        'Intuitive design standards',
                        'Accessibility requirements',
                        'Voice and gesture control adoption'
                    ]
                }
            ],
            'industry_specific_forecasts': {
                'furniture': [
                    {
                        'name': 'Adaptive Living Spaces',
                        'description': 'Furniture that transforms to accommodate changing needs',
                        'probability': 0.8,
                        'estimated_timeline': '2-4 years',
                        'key_indicators': [
                            'Robotic furniture elements',
                            'Space optimization focus',
                            'Multi-modal functionality',
                            'Smart adaptation systems'
                        ]
                    },
                    {
                        'name': 'Hyper-Local Production',
                        'description': 'Furniture produced within very close proximity to end users',
                        'probability': 0.7,
                        'estimated_timeline': '3-5 years',
                        'key_indicators': [
                            'Distributed manufacturing',
                            'Local material sourcing',
                            'On-demand production',
                            'Community-based making'
                        ]
                    }
                ],
                'electronics': [
                    {
                        'name': 'Ambient Computing',
                        'description': 'Technology that fades into the background of everyday life',
                        'probability': 0.85,
                        'estimated_timeline': '2-3 years',
                        'key_indicators': [
                            'Invisible interfaces',
                            'Context-aware systems',
                            'Predictive functionality',
                            'Environmental integration'
                        ]
                    },
                    {
                        'name': 'Energy Harvesting Devices',
                        'description': 'Electronics that generate their own power from ambient sources',
                        'probability': 0.65,
                        'estimated_timeline': '3-6 years',
                        'key_indicators': [
                            'Kinetic energy capture',
                            'Solar integration',
                            'Thermal energy harvesting',
                            'RF energy collection'
                        ]
                    }
                ],
                'packaging': [
                    {
                        'name': 'Interactive Packaging',
                        'description': 'Packaging that provides digital experiences and information',
                        'probability': 0.75,
                        'estimated_timeline': '1-3 years',
                        'key_indicators': [
                            'AR-enabled packaging',
                            'NFC/RFID integration',
                            'Dynamic information display',
                            'Consumer engagement features'
                        ]
                    },
                    {
                        'name': 'Zero-Waste Systems',
                        'description': 'Packaging systems that eliminate waste entirely',
                        'probability': 0.7,
                        'estimated_timeline': '3-5 years',
                        'key_indicators': [
                            'Closed-loop material flows',
                            'Packaging service models',
                            'Edible or dissolvable materials',
                            'Reuse infrastructure'
                        ]
                    }
                ]
            }
        }
        
        logger.info("Initialized default trend database")
    
    def save_database(self, output_path=None):
        """
        Save the trend database to a file.
        
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
                    'trends': self.trends,
                    'industry_trends': self.industry_trends,
                    'consumer_preferences': self.consumer_preferences,
                    'trend_forecasts': self.trend_forecasts,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"Saved trend database to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving trend database: {str(e)}")
            return False
    
    def get_global_trends(self, min_strength=0.0, sort_by='strength'):
        """
        Get global design trends, optionally filtered by minimum strength.
        
        Args:
            min_strength (float): Minimum trend strength (0-1)
            sort_by (str): Field to sort by ('strength', 'growth_rate')
            
        Returns:
            list: Global design trends
        """
        # Filter and sort trends
        filtered_trends = []
        
        for trend_id, trend in self.trends.items():
            if trend.get('strength', 0) >= min_strength:
                trend_data = trend.copy()
                trend_data['id'] = trend_id
                filtered_trends.append(trend_data)
        
        # Sort trends
        if sort_by == 'strength':
            filtered_trends.sort(key=lambda x: x.get('strength', 0), reverse=True)
        elif sort_by == 'growth_rate':
            filtered_trends.sort(key=lambda x: x.get('growth_rate', 0), reverse=True)
        
        return filtered_trends
    
    def get_industry_trends(self, industry, min_strength=0.0, sort_by='strength'):
        """
        Get trends for a specific industry, optionally filtered by minimum strength.
        
        Args:
            industry (str): Industry name
            min_strength (float): Minimum trend strength (0-1)
            sort_by (str): Field to sort by ('strength', 'growth_rate')
            
        Returns:
            list: Industry-specific trends
        """
        if industry not in self.industry_trends:
            return []
        
        # Filter and sort industry trends
        filtered_trends = []
        
        for trend_id, trend in self.industry_trends[industry].items():
            if trend.get('strength', 0) >= min_strength:
                trend_data = trend.copy()
                trend_data['id'] = trend_id
                trend_data['industry'] = industry
                filtered_trends.append(trend_data)
        
        # Sort trends
        if sort_by == 'strength':
            filtered_trends.sort(key=lambda x: x.get('strength', 0), reverse=True)
        elif sort_by == 'growth_rate':
            filtered_trends.sort(key=lambda x: x.get('growth_rate', 0), reverse=True)
        
        return filtered_trends
    
    def get_consumer_preferences(self, demographic=None, region=None):
        """
        Get consumer preferences, optionally filtered by demographic and region.
        
        Args:
            demographic (str, optional): Demographic group ('gen_z', 'millennials', 'gen_x', 'boomers')
            region (str, optional): Geographic region
            
        Returns:
            dict: Consumer preferences
        """
        preferences = {}
        
        for pref_id, pref_data in self.consumer_preferences.items():
            pref_value = pref_data.get('importance', 0)
            
            # Adjust for demographic if specified
            if demographic and demographic in pref_data.get('demographic_variations', {}):
                pref_value = pref_data['demographic_variations'][demographic]
            
            # Adjust for region if specified
            if region and region in pref_data.get('regional_variations', {}):
                # Average with regional value
                regional_value = pref_data['regional_variations'][region]
                pref_value = (pref_value + regional_value) / 2
            
            preferences[pref_id] = {
                'value': pref_value,
                'growth_rate': pref_data.get('growth_rate', 0),
                'key_factors': pref_data.get('key_factors', [])
            }
        
        return preferences
    
    def get_emerging_trends(self, min_probability=0.0):
        """
        Get emerging trends, optionally filtered by minimum probability.
        
        Args:
            min_probability (float): Minimum trend probability (0-1)
            
        Returns:
            list: Emerging trends
        """
        # Filter emerging trends
        filtered_trends = []
        
        for trend in self.trend_forecasts.get('emerging_trends', []):
            if trend.get('probability', 0) >= min_probability:
                filtered_trends.append(trend)
        
        # Sort by probability (descending)
        filtered_trends.sort(key=lambda x: x.get('probability', 0), reverse=True)
        
        return filtered_trends
    
    def get_industry_forecasts(self, industry, min_probability=0.0):
        """
        Get forecasts for a specific industry, optionally filtered by minimum probability.
        
        Args:
            industry (str): Industry name
            min_probability (float): Minimum forecast probability (0-1)
            
        Returns:
            list: Industry-specific forecasts
        """
        industry_forecasts = self.trend_forecasts.get('industry_specific_forecasts', {}).get(industry, [])
        
        # Filter forecasts
        filtered_forecasts = []
        
        for forecast in industry_forecasts:
            if forecast.get('probability', 0) >= min_probability:
                filtered_forecasts.append(forecast)
        
        # Sort by probability (descending)
        filtered_forecasts.sort(key=lambda x: x.get('probability', 0), reverse=True)
        
        return filtered_forecasts
    
    def analyze_trend_alignment(self, product_data):
        """
        Analyze how well a product aligns with current trends.
        
        Args:
            product_data (dict): Product design data
            
        Returns:
            dict: Trend alignment analysis
        """
        try:
            # Extract product attributes
            attributes = product_data.get('attributes', {})
            industry = product_data.get('industry', '')
            target_demographic = product_data.get('target_demographic', '')
            target_region = product_data.get('target_region', '')
            
            if not attributes:
                return {
                    'product': product_data.get('name', 'Unknown'),
                    'overall_alignment': 0,
                    'error': 'No attributes found in product data'
                }
            
            # Get relevant trends
            global_trends = self.get_global_trends(min_strength=0.7)
            industry_trends = self.get_industry_trends(industry, min_strength=0.7) if industry else []
            
            # Analyze alignment with global trends
            global_alignments = []
            
            for trend in global_trends:
                alignment = self._calculate_trend_alignment(attributes, trend)
                if alignment['score'] > 0:
                    global_alignments.append(alignment)
            
            # Analyze alignment with industry trends
            industry_alignments = []
            
            for trend in industry_trends:
                alignment = self._calculate_trend_alignment(attributes, trend)
                if alignment['score'] > 0:
                    industry_alignments.append(alignment)
            
            # Calculate overall alignment score
            all_alignments = global_alignments + industry_alignments
            if all_alignments:
                overall_score = sum(a['score'] for a in all_alignments) / len(all_alignments)
            else:
                overall_score = 0
            
            # Determine alignment level
            if overall_score >= 0.8:
                alignment_level = 'Excellent'
            elif overall_score >= 0.6:
                alignment_level = 'Good'
            elif overall_score >= 0.4:
                alignment_level = 'Moderate'
            elif overall_score >= 0.2:
                alignment_level = 'Low'
            else:
                alignment_level = 'Poor'
            
            # Get consumer preferences
            preferences = self.get_consumer_preferences(target_demographic, target_region)
            
            # Generate recommendations
            recommendations = self._generate_trend_recommendations(attributes, global_trends, industry_trends, preferences)
            
            # Create analysis result
            analysis = {
                'product': product_data.get('name', 'Unknown'),
                'overall_alignment': round(overall_score * 100, 1),
                'alignment_level': alignment_level,
                'global_trend_alignments': global_alignments,
                'industry_trend_alignments': industry_alignments,
                'recommendations': recommendations
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trend alignment: {str(e)}")
            return {
                'product': product_data.get('name', 'Unknown'),
                'overall_alignment': 0,
                'error': str(e)
            }
    
    def _calculate_trend_alignment(self, attributes, trend):
        """
        Calculate alignment between product attributes and a trend.
        
        Args:
            attributes (dict): Product attributes
            trend (dict): Trend data
            
        Returns:
            dict: Alignment information
        """
        # Extract trend elements
        trend_elements = trend.get('key_elements', [])
        if not trend_elements:
            return {
                'trend': trend.get('name'),
                'score': 0,
                'matching_elements': [],
                'missing_elements': []
            }
        
        # Check for matching elements
        matching_elements = []
        missing_elements = []
        
        for element in trend_elements:
            element_lower = element.lower()
            
            # Check if element is present in any attribute
            found = False
            for attr_name, attr_value in attributes.items():
                if isinstance(attr_value, str) and any(keyword in attr_value.lower() for keyword in element_lower.split()):
                    matching_elements.append(element)
                    found = True
                    break
                elif isinstance(attr_value, list) and any(keyword in ' '.join(attr_value).lower() for keyword in element_lower.split()):
                    matching_elements.append(element)
                    found = True
                    break
                elif isinstance(attr_value, bool) and attr_value and any(keyword in attr_name.lower() for keyword in element_lower.split()):
                    matching_elements.append(element)
                    found = True
                    break
            
            if not found:
                missing_elements.append(element)
        
        # Calculate alignment score
        if trend_elements:
            alignment_score = len(matching_elements) / len(trend_elements)
        else:
            alignment_score = 0
        
        # Create alignment result
        alignment = {
            'trend': trend.get('name'),
            'score': alignment_score,
            'matching_elements': matching_elements,
            'missing_elements': missing_elements
        }
        
        return alignment
    
    def _generate_trend_recommendations(self, attributes, global_trends, industry_trends, preferences):
        """
        Generate trend-based recommendations for product improvement.
        
        Args:
            attributes (dict): Product attributes
            global_trends (list): Global design trends
            industry_trends (list): Industry-specific trends
            preferences (dict): Consumer preferences
            
        Returns:
            list: Trend recommendations
        """
        recommendations = []
        
        # Find trends with low alignment but high strength/growth
        potential_trends = []
        
        for trend in global_trends + industry_trends:
            alignment = self._calculate_trend_alignment(attributes, trend)
            if alignment['score'] < 0.5 and trend.get('strength', 0) >= 0.7:
                potential_trends.append({
                    'trend': trend,
                    'alignment': alignment,
                    'priority': trend.get('strength', 0) * (1 + trend.get('growth_rate', 0))
                })
        
        # Sort by priority (descending)
        potential_trends.sort(key=lambda x: x['priority'], reverse=True)
        
        # Generate recommendations for top trends
        for trend_data in potential_trends[:3]:
            trend = trend_data['trend']
            alignment = trend_data['alignment']
            
            # Create recommendation
            recommendation = {
                'type': 'trend_alignment',
                'trend': trend.get('name'),
                'description': trend.get('description'),
                'current_alignment': f"{int(alignment['score'] * 100)}%",
                'trend_strength': trend.get('strength', 0),
                'trend_growth': trend.get('growth_rate', 0),
                'suggested_elements': alignment['missing_elements'][:3],
                'potential_impact': 'High' if trend.get('strength', 0) >= 0.8 else 'Medium'
            }
            
            recommendations.append(recommendation)
        
        # Add recommendations based on consumer preferences
        high_preference_categories = []
        
        for pref_id, pref_data in preferences.items():
            if pref_data['value'] >= 0.8:
                high_preference_categories.append({
                    'category': pref_id,
                    'value': pref_data['value'],
                    'growth_rate': pref_data['growth_rate'],
                    'key_factors': pref_data['key_factors']
                })
        
        # Sort by preference value (descending)
        high_preference_categories.sort(key=lambda x: x['value'], reverse=True)
        
        # Generate recommendations for top preferences
        for pref in high_preference_categories[:2]:
            # Create recommendation
            recommendation = {
                'type': 'consumer_preference',
                'preference': pref['category'].replace('_', ' ').title(),
                'importance': f"{int(pref['value'] * 100)}%",
                'growth_rate': pref['growth_rate'],
                'key_factors': pref['key_factors'][:3],
                'potential_impact': 'High'
            }
            
            recommendations.append(recommendation)
        
        # Add emerging trend recommendation if relevant
        emerging_trends = self.get_emerging_trends(min_probability=0.75)
        if emerging_trends:
            top_emerging = emerging_trends[0]
            
            recommendation = {
                'type': 'emerging_trend',
                'trend': top_emerging.get('name'),
                'description': top_emerging.get('description'),
                'probability': top_emerging.get('probability', 0),
                'timeline': top_emerging.get('estimated_timeline'),
                'key_indicators': top_emerging.get('key_indicators', [])[:3],
                'potential_impact': top_emerging.get('potential_impact', 'Medium')
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def generate_trend_report(self, industry=None):
        """
        Generate a comprehensive trend report, optionally for a specific industry.
        
        Args:
            industry (str, optional): Industry to focus on
            
        Returns:
            dict: Trend report
        """
        # Get global trends
        global_trends = self.get_global_trends(min_strength=0.6, sort_by='strength')
        
        # Get industry trends if specified
        industry_trends = []
        if industry:
            industry_trends = self.get_industry_trends(industry, min_strength=0.6, sort_by='strength')
        
        # Get emerging trends
        emerging_trends = self.get_emerging_trends(min_probability=0.6)
        
        # Get industry forecasts if specified
        industry_forecasts = []
        if industry:
            industry_forecasts = self.get_industry_forecasts(industry, min_probability=0.6)
        
        # Get declining trends
        declining_trends = self.trend_forecasts.get('declining_trends', [])
        
        # Create trend report
        report = {
            'report_date': datetime.now().isoformat(),
            'industry_focus': industry,
            'summary': self._generate_trend_summary(global_trends, industry_trends, emerging_trends),
            'global_trends': global_trends,
            'industry_trends': industry_trends,
            'emerging_trends': emerging_trends,
            'industry_forecasts': industry_forecasts,
            'declining_trends': declining_trends,
            'design_implications': self._generate_design_implications(global_trends, industry_trends, emerging_trends)
        }
        
        return report
    
    def _generate_trend_summary(self, global_trends, industry_trends, emerging_trends):
        """
        Generate a summary of key trends.
        
        Args:
            global_trends (list): Global design trends
            industry_trends (list): Industry-specific trends
            emerging_trends (list): Emerging trends
            
        Returns:
            str: Trend summary
        """
        # Get top trends
        top_global = global_trends[:3] if global_trends else []
        top_industry = industry_trends[:3] if industry_trends else []
        top_emerging = emerging_trends[:2] if emerging_trends else []
        
        # Create summary
        summary = "Current design landscape is characterized by "
        
        if top_global:
            trend_names = [t['name'] for t in top_global]
            summary += f"strong global trends in {', '.join(trend_names[:-1]) + ' and ' + trend_names[-1] if len(trend_names) > 1 else trend_names[0]}"
        
        if top_industry:
            if top_global:
                summary += ", with industry-specific focus on "
            else:
                summary += "industry-specific focus on "
            
            trend_names = [t['name'] for t in top_industry]
            summary += f"{', '.join(trend_names[:-1]) + ' and ' + trend_names[-1] if len(trend_names) > 1 else trend_names[0]}"
        
        if top_emerging:
            if top_global or top_industry:
                summary += ". Emerging trends to watch include "
            else:
                summary += "emerging trends including "
            
            trend_names = [t['name'] for t in top_emerging]
            summary += f"{', '.join(trend_names[:-1]) + ' and ' + trend_names[-1] if len(trend_names) > 1 else trend_names[0]}"
        
        summary += "."
        
        return summary
    
    def _generate_design_implications(self, global_trends, industry_trends, emerging_trends):
        """
        Generate design implications based on trends.
        
        Args:
            global_trends (list): Global design trends
            industry_trends (list): Industry-specific trends
            emerging_trends (list): Emerging trends
            
        Returns:
            list: Design implications
        """
        implications = []
        
        # Add implications for top global trends
        for trend in global_trends[:3]:
            implication = {
                'trend': trend.get('name'),
                'implication': self._generate_implication_for_trend(trend),
                'priority': 'High' if trend.get('strength', 0) >= 0.8 else 'Medium'
            }
            implications.append(implication)
        
        # Add implications for top industry trends
        for trend in industry_trends[:3]:
            implication = {
                'trend': trend.get('name'),
                'implication': self._generate_implication_for_trend(trend),
                'priority': 'High' if trend.get('strength', 0) >= 0.8 else 'Medium'
            }
            implications.append(implication)
        
        # Add implications for top emerging trends
        for trend in emerging_trends[:2]:
            implication = {
                'trend': trend.get('name'),
                'implication': self._generate_implication_for_trend(trend),
                'priority': 'Medium',
                'timeline': trend.get('estimated_timeline')
            }
            implications.append(implication)
        
        return implications
    
    def _generate_implication_for_trend(self, trend):
        """
        Generate design implication for a specific trend.
        
        Args:
            trend (dict): Trend data
            
        Returns:
            str: Design implication
        """
        # Get trend elements
        elements = trend.get('key_elements', [])
        
        if not elements:
            return f"Consider incorporating aspects of {trend.get('name')} into product design."
        
        # Select random elements (2-3)
        num_elements = min(len(elements), random.randint(2, 3))
        selected_elements = random.sample(elements, num_elements)
        
        # Generate implication
        implication = f"Design should incorporate {', '.join(selected_elements[:-1]) + ' and ' + selected_elements[-1] if len(selected_elements) > 1 else selected_elements[0]}"
        
        # Add examples if available
        examples = trend.get('examples', [])
        if examples:
            num_examples = min(len(examples), 2)
            selected_examples = random.sample(examples, num_examples)
            implication += f", similar to {', '.join(selected_examples)}"
        
        implication += "."
        
        return implication
    
    def add_trend(self, trend_id, trend_data, trend_type='global'):
        """
        Add a new trend to the database.
        
        Args:
            trend_id (str): Trend identifier
            trend_data (dict): Trend information
            trend_type (str): Type of trend ('global', 'industry', 'emerging')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate trend data
            required_fields = ['name', 'description']
            for field in required_fields:
                if field not in trend_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add trend to appropriate collection
            if trend_type == 'global':
                self.trends[trend_id] = trend_data
                logger.info(f"Added global trend: {trend_id}")
            elif trend_type == 'industry':
                industry = trend_data.get('industry')
                if not industry:
                    logger.error("Missing industry for industry trend")
                    return False
                
                if industry not in self.industry_trends:
                    self.industry_trends[industry] = {}
                
                self.industry_trends[industry][trend_id] = trend_data
                logger.info(f"Added industry trend: {trend_id} for {industry}")
            elif trend_type == 'emerging':
                self.trend_forecasts['emerging_trends'].append(trend_data)
                logger.info(f"Added emerging trend: {trend_data.get('name')}")
            else:
                logger.error(f"Invalid trend type: {trend_type}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding trend: {str(e)}")
            return False
    
    def update_trend(self, trend_id, trend_data, trend_type='global'):
        """
        Update an existing trend in the database.
        
        Args:
            trend_id (str): Trend identifier
            trend_data (dict): Updated trend information
            trend_type (str): Type of trend ('global', 'industry')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Update trend in appropriate collection
            if trend_type == 'global':
                if trend_id not in self.trends:
                    logger.error(f"Global trend not found: {trend_id}")
                    return False
                
                self.trends[trend_id].update(trend_data)
                logger.info(f"Updated global trend: {trend_id}")
            elif trend_type == 'industry':
                industry = trend_data.get('industry')
                if not industry or industry not in self.industry_trends or trend_id not in self.industry_trends[industry]:
                    logger.error(f"Industry trend not found: {trend_id}")
                    return False
                
                self.industry_trends[industry][trend_id].update(trend_data)
                logger.info(f"Updated industry trend: {trend_id} for {industry}")
            else:
                logger.error(f"Invalid trend type: {trend_type}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating trend: {str(e)}")
            return False
    
    def delete_trend(self, trend_id, trend_type='global', industry=None):
        """
        Delete a trend from the database.
        
        Args:
            trend_id (str): Trend identifier
            trend_type (str): Type of trend ('global', 'industry')
            industry (str, optional): Industry for industry trends
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete trend from appropriate collection
            if trend_type == 'global':
                if trend_id not in self.trends:
                    logger.error(f"Global trend not found: {trend_id}")
                    return False
                
                del self.trends[trend_id]
                logger.info(f"Deleted global trend: {trend_id}")
            elif trend_type == 'industry':
                if not industry or industry not in self.industry_trends or trend_id not in self.industry_trends[industry]:
                    logger.error(f"Industry trend not found: {trend_id}")
                    return False
                
                del self.industry_trends[industry][trend_id]
                logger.info(f"Deleted industry trend: {trend_id} for {industry}")
            else:
                logger.error(f"Invalid trend type: {trend_type}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting trend: {str(e)}")
            return False


if __name__ == "__main__":
    # Example usage
    analyzer = TrendAnalyzer()
    
    # Get global trends
    global_trends = analyzer.get_global_trends(min_strength=0.7)
    print(f"Found {len(global_trends)} strong global trends")
    
    # Get industry trends
    furniture_trends = analyzer.get_industry_trends('furniture')
    print(f"Found {len(furniture_trends)} furniture industry trends")
    
    # Get consumer preferences
    preferences = analyzer.get_consumer_preferences('millennials', 'north_america')
    print(f"Found {len(preferences)} consumer preferences for millennials in North America")
    
    # Generate trend report
    report = analyzer.generate_trend_report('furniture')
    print(f"Generated trend report with {len(report['design_implications'])} design implications")
