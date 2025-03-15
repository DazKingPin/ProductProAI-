import logging
import json
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComplianceChecker:
    """
    Class for checking product designs against industry standards and regulations.
    Ensures that designs meet safety, usability, and environmental guidelines.
    """
    
    def __init__(self, standards_service=None, database_path=None):
        """
        Initialize the ComplianceChecker.
        
        Args:
            standards_service: Reference to the IndustryStandards service
            database_path (str, optional): Path to the compliance database file
        """
        logger.info("Initializing ComplianceChecker")
        self.standards_service = standards_service
        self.database_path = database_path
        self.regulations = {}
        self.compliance_rules = {}
        self.certification_requirements = {}
        self._load_compliance_data()
    
    def _load_compliance_data(self):
        """
        Load compliance data from database file or initialize with default data.
        """
        try:
            if self.database_path and os.path.exists(self.database_path):
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    self.regulations = data.get('regulations', {})
                    self.compliance_rules = data.get('compliance_rules', {})
                    self.certification_requirements = data.get('certification_requirements', {})
                logger.info(f"Loaded compliance data from database")
            else:
                logger.info("Initializing default compliance database")
                self._initialize_default_data()
        except Exception as e:
            logger.error(f"Error loading compliance data: {str(e)}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """
        Initialize the database with default compliance data.
        """
        # Initialize regulations by region and industry
        self.regulations = {
            'global': {
                'iso_9001': {
                    'name': 'ISO 9001',
                    'description': 'Quality management systems standard',
                    'scope': 'All industries',
                    'key_requirements': [
                        'Documented quality management system',
                        'Management commitment to quality',
                        'Customer focus',
                        'Continuous improvement',
                        'Process approach to management'
                    ],
                    'url': 'https://www.iso.org/iso-9001-quality-management.html'
                },
                'iso_14001': {
                    'name': 'ISO 14001',
                    'description': 'Environmental management systems standard',
                    'scope': 'All industries',
                    'key_requirements': [
                        'Environmental policy',
                        'Environmental aspects identification',
                        'Legal and other requirements',
                        'Environmental objectives and targets',
                        'Environmental management program'
                    ],
                    'url': 'https://www.iso.org/iso-14001-environmental-management.html'
                }
            },
            'north_america': {
                'usa': {
                    'cpsc': {
                        'name': 'Consumer Product Safety Commission Regulations',
                        'description': 'Federal regulations for consumer product safety',
                        'scope': 'Consumer products',
                        'key_requirements': [
                            'Product safety testing',
                            'Hazard analysis',
                            'Warning labels',
                            'Recall procedures',
                            'Reporting requirements'
                        ],
                        'url': 'https://www.cpsc.gov/Regulations-Laws--Standards'
                    },
                    'fda': {
                        'name': 'Food and Drug Administration Regulations',
                        'description': 'Regulations for food, drugs, medical devices, and cosmetics',
                        'scope': 'Food, drugs, medical devices, cosmetics',
                        'key_requirements': [
                            'Good Manufacturing Practices (GMP)',
                            'Safety testing',
                            'Labeling requirements',
                            'Registration and listing',
                            'Adverse event reporting'
                        ],
                        'url': 'https://www.fda.gov/regulatory-information'
                    },
                    'fcc': {
                        'name': 'Federal Communications Commission Regulations',
                        'description': 'Regulations for electronic and communication devices',
                        'scope': 'Electronics, communication devices',
                        'key_requirements': [
                            'Radio frequency emissions compliance',
                            'Equipment authorization',
                            'Technical standards',
                            'Labeling requirements',
                            'Testing procedures'
                        ],
                        'url': 'https://www.fcc.gov/wireless/bureau-divisions/technologies-systems-and-innovation-division/rules-regulations-title-47'
                    }
                },
                'canada': {
                    'health_canada': {
                        'name': 'Health Canada Regulations',
                        'description': 'Regulations for consumer products, food, and health products',
                        'scope': 'Consumer products, food, health products',
                        'key_requirements': [
                            'Product safety requirements',
                            'Labeling standards',
                            'Hazardous products regulations',
                            'Testing and certification',
                            'Reporting requirements'
                        ],
                        'url': 'https://www.canada.ca/en/health-canada/corporate/about-health-canada/legislation-guidelines.html'
                    }
                }
            },
            'europe': {
                'eu': {
                    'ce_marking': {
                        'name': 'CE Marking Requirements',
                        'description': 'Mandatory conformity marking for products sold in the European Economic Area',
                        'scope': 'Various product categories',
                        'key_requirements': [
                            'Essential health and safety requirements',
                            'Technical documentation',
                            'Declaration of conformity',
                            'Conformity assessment',
                            'CE marking affixation'
                        ],
                        'url': 'https://ec.europa.eu/growth/single-market/ce-marking_en'
                    },
                    'rohs': {
                        'name': 'RoHS Directive',
                        'description': 'Restriction of Hazardous Substances in electrical and electronic equipment',
                        'scope': 'Electrical and electronic equipment',
                        'key_requirements': [
                            'Restricted substances limits',
                            'Technical documentation',
                            'Declaration of conformity',
                            'CE marking',
                            'Material testing'
                        ],
                        'url': 'https://ec.europa.eu/environment/topics/waste-and-recycling/rohs-directive_en'
                    },
                    'reach': {
                        'name': 'REACH Regulation',
                        'description': 'Registration, Evaluation, Authorization and Restriction of Chemicals',
                        'scope': 'Chemical substances',
                        'key_requirements': [
                            'Registration of substances',
                            'Safety data sheets',
                            'Authorization for substances of very high concern',
                            'Restrictions on hazardous substances',
                            'Information communication in supply chain'
                        ],
                        'url': 'https://echa.europa.eu/regulations/reach/understanding-reach'
                    },
                    'weee': {
                        'name': 'WEEE Directive',
                        'description': 'Waste Electrical and Electronic Equipment Directive',
                        'scope': 'Electrical and electronic equipment',
                        'key_requirements': [
                            'Product marking',
                            'Information for users',
                            'Separate collection',
                            'Treatment requirements',
                            'Recovery targets'
                        ],
                        'url': 'https://ec.europa.eu/environment/topics/waste-and-recycling/waste-electrical-and-electronic-equipment-weee_en'
                    }
                }
            },
            'asia': {
                'china': {
                    'ccc': {
                        'name': 'China Compulsory Certification (CCC)',
                        'description': 'Mandatory certification for products sold in China',
                        'scope': 'Various product categories',
                        'key_requirements': [
                            'Product testing',
                            'Factory inspection',
                            'CCC mark application',
                            'Technical documentation',
                            'Follow-up inspections'
                        ],
                        'url': 'http://www.cnca.gov.cn/cnca/cxzq/cccbz/'
                    }
                },
                'japan': {
                    'pse': {
                        'name': 'Product Safety Electrical Appliance & Material (PSE) Mark',
                        'description': 'Mandatory certification for electrical products in Japan',
                        'scope': 'Electrical products',
                        'key_requirements': [
                            'Product testing',
                            'Technical standards compliance',
                            'PSE mark application',
                            'Technical documentation',
                            'Factory inspection'
                        ],
                        'url': 'https://www.meti.go.jp/english/policy/economy/consumer/pse/index.html'
                    }
                }
            }
        }
        
        # Initialize industry-specific compliance rules
        self.compliance_rules = {
            'furniture': {
                'safety': [
                    {
                        'name': 'Stability Requirements',
                        'description': 'Requirements to prevent tipping and ensure stability',
                        'applicable_standards': ['ANSI/BIFMA X5.1', 'EN 1730'],
                        'test_methods': [
                            'Stability under vertical load',
                            'Stability with drawers open',
                            'Stability on uneven surfaces'
                        ],
                        'severity': 'Critical'
                    },
                    {
                        'name': 'Sharp Edge Prevention',
                        'description': 'Requirements to prevent injuries from sharp edges',
                        'applicable_standards': ['ANSI/BIFMA X5.1', 'EN 12520'],
                        'test_methods': [
                            'Edge sharpness test',
                            'Corner radius measurement'
                        ],
                        'severity': 'Critical'
                    },
                    {
                        'name': 'Load Capacity',
                        'description': 'Requirements for weight-bearing capacity',
                        'applicable_standards': ['ANSI/BIFMA X5.1', 'EN 1730'],
                        'test_methods': [
                            'Static load test',
                            'Dynamic load test',
                            'Impact test'
                        ],
                        'severity': 'Critical'
                    }
                ],
                'materials': [
                    {
                        'name': 'Formaldehyde Emissions',
                        'description': 'Limits on formaldehyde emissions from composite wood products',
                        'applicable_standards': ['CARB Phase 2', 'EPA TSCA Title VI'],
                        'test_methods': [
                            'ASTM E1333',
                            'ASTM D6007'
                        ],
                        'severity': 'High'
                    },
                    {
                        'name': 'Flame Retardancy',
                        'description': 'Requirements for flame retardant properties of upholstered furniture',
                        'applicable_standards': ['California TB 117-2013', 'BS 5852'],
                        'test_methods': [
                            'Cigarette test',
                            'Match test',
                            'Open flame test'
                        ],
                        'severity': 'High'
                    }
                ],
                'ergonomics': [
                    {
                        'name': 'Seating Dimensions',
                        'description': 'Requirements for ergonomic seating dimensions',
                        'applicable_standards': ['ANSI/HFES 100', 'EN 1335'],
                        'test_methods': [
                            'Seat height measurement',
                            'Seat depth measurement',
                            'Backrest dimensions'
                        ],
                        'severity': 'Medium'
                    }
                ]
            },
            'electronics': {
                'safety': [
                    {
                        'name': 'Electrical Safety',
                        'description': 'Requirements to prevent electrical hazards',
                        'applicable_standards': ['IEC 60950', 'UL 60950'],
                        'test_methods': [
                            'Dielectric voltage withstand test',
                            'Leakage current test',
                            'Grounding continuity test'
                        ],
                        'severity': 'Critical'
                    },
                    {
                        'name': 'Thermal Safety',
                        'description': 'Requirements to prevent overheating and fire hazards',
                        'applicable_standards': ['IEC 60950', 'UL 60950'],
                        'test_methods': [
                            'Temperature rise test',
                            'Abnormal operation test',
                            'Thermal cycling test'
                        ],
                        'severity': 'Critical'
                    }
                ],
                'emissions': [
                    {
                        'name': 'Electromagnetic Compatibility (EMC)',
                        'description': 'Requirements for electromagnetic emissions and immunity',
                        'applicable_standards': ['FCC Part 15', 'CISPR 22', 'EN 55022'],
                        'test_methods': [
                            'Radiated emissions test',
                            'Conducted emissions test',
                            'Immunity test'
                        ],
                        'severity': 'High'
                    }
                ],
                'materials': [
                    {
                        'name': 'Hazardous Substances',
                        'description': 'Restrictions on hazardous substances in electronics',
                        'applicable_standards': ['RoHS Directive', 'REACH Regulation'],
                        'test_methods': [
                            'XRF screening',
                            'Chemical analysis',
                            'Material composition verification'
                        ],
                        'severity': 'High'
                    }
                ],
                'energy': [
                    {
                        'name': 'Energy Efficiency',
                        'description': 'Requirements for energy consumption and efficiency',
                        'applicable_standards': ['Energy Star', 'ErP Directive'],
                        'test_methods': [
                            'Power consumption measurement',
                            'Standby power measurement',
                            'Efficiency calculation'
                        ],
                        'severity': 'Medium'
                    }
                ]
            },
            'packaging': {
                'materials': [
                    {
                        'name': 'Heavy Metals',
                        'description': 'Restrictions on heavy metals in packaging materials',
                        'applicable_standards': ['EU Packaging Directive', 'CONEG'],
                        'test_methods': [
                            'Chemical analysis',
                            'XRF screening'
                        ],
                        'severity': 'High'
                    },
                    {
                        'name': 'Recyclability',
                        'description': 'Requirements for recyclable packaging materials',
                        'applicable_standards': ['ISO 18604', 'EU Packaging Directive'],
                        'test_methods': [
                            'Material identification',
                            'Separation test',
                            'Recycling process compatibility'
                        ],
                        'severity': 'Medium'
                    }
                ],
                'labeling': [
                    {
                        'name': 'Recycling Symbols',
                        'description': 'Requirements for recycling symbols and markings',
                        'applicable_standards': ['ISO 14021', 'EU Packaging Directive'],
                        'test_methods': [
                            'Symbol verification',
                            'Material identification code check'
                        ],
                        'severity': 'Low'
                    }
                ],
                'performance': [
                    {
                        'name': 'Protection Performance',
                        'description': 'Requirements for protective performance of packaging',
                        'applicable_standards': ['ISTA Procedures', 'ASTM D4169'],
                        'test_methods': [
                            'Drop test',
                            'Vibration test',
                            'Compression test'
                        ],
                        'severity': 'Medium'
                    }
                ]
            },
            'fashion': {
                'materials': [
                    {
                        'name': 'Restricted Substances',
                        'description': 'Restrictions on hazardous substances in textiles',
                        'applicable_standards': ['REACH Regulation', 'OEKO-TEX Standard 100'],
                        'test_methods': [
                            'Chemical analysis',
                            'Extraction test',
                            'pH measurement'
                        ],
                        'severity': 'High'
                    },
                    {
                        'name': 'Azo Dyes',
                        'description': 'Restrictions on azo dyes that can release carcinogenic amines',
                        'applicable_standards': ['EU Directive 2002/61/EC', 'REACH Regulation'],
                        'test_methods': [
                            'Extraction and chromatography',
                            'Mass spectrometry'
                        ],
                        'severity': 'Critical'
                    }
                ],
                'safety': [
                    {
                        'name': 'Flammability',
                        'description': 'Requirements for flame resistance of textiles',
                        'applicable_standards': ['16 CFR Part 1610', 'EN ISO 14116'],
                        'test_methods': [
                            'Vertical flame test',
                            'Surface flash test',
                            'Burning behavior test'
                        ],
                        'severity': 'Critical'
                    },
                    {
                        'name': 'Children\'s Clothing Safety',
                        'description': 'Safety requirements for children\'s clothing',
                        'applicable_standards': ['ASTM F1816', 'EN 14682'],
                        'test_methods': [
                            'Drawstring measurement',
                            'Small parts test',
                            'Sharp point test'
                        ],
                        'severity': 'Critical'
                    }
                ],
                'labeling': [
                    {
                        'name': 'Fiber Content',
                        'description': 'Requirements for fiber content labeling',
                        'applicable_standards': ['Textile Fiber Products Identification Act', 'EU Regulation 1007/2011'],
                        'test_methods': [
                            'Fiber identification',
                            'Quantitative analysis',
                            'Label verification'
                        ],
                        'severity': 'Medium'
                    },
                    {
                        'name': 'Care Instructions',
                        'description': 'Requirements for care labeling',
                        'applicable_standards': ['ISO 3758', '16 CFR Part 423'],
                        'test_methods': [
                            'Symbol verification',
                            'Washing test',
                            'Drying test'
                        ],
                        'severity': 'Medium'
                    }
                ]
            }
        }
        
        # Initialize certification requirements
        self.certification_requirements = {
            'furniture': {
                'ansi_bifma': {
                    'name': 'ANSI/BIFMA Certification',
                    'description': 'Certification for commercial furniture',
                    'requirements': [
                        'Product testing by accredited laboratory',
                        'Compliance with ANSI/BIFMA standards',
                        'Documentation of test results',
                        'Periodic retesting'
                    ],
                    'url': 'https://www.bifma.org/page/standards'
                },
                'greenguard': {
                    'name': 'GREENGUARD Certification',
                    'description': 'Certification for low chemical emissions',
                    'requirements': [
                        'Chemical emissions testing',
                        'Compliance with emission limits',
                        'Documentation of test results',
                        'Annual recertification'
                    ],
                    'url': 'https://www.ul.com/resources/ul-greenguard-certification-program'
                },
                'fsc': {
                    'name': 'Forest Stewardship Council (FSC) Certification',
                    'description': 'Certification for responsibly sourced wood',
                    'requirements': [
                        'Chain of custody documentation',
                        'Compliance with FSC standards',
                        'Third-party verification',
                        'Annual audits'
                    ],
                    'url': 'https://fsc.org/en/certification'
                }
            },
            'electronics': {
                'energy_star': {
                    'name': 'ENERGY STAR Certification',
                    'description': 'Certification for energy-efficient products',
                    'requirements': [
                        'Energy efficiency testing',
                        'Compliance with ENERGY STAR specifications',
                        'Documentation of test results',
                        'Verification testing'
                    ],
                    'url': 'https://www.energystar.gov/products'
                },
                'ul': {
                    'name': 'UL Certification',
                    'description': 'Safety certification for electrical products',
                    'requirements': [
                        'Product safety testing',
                        'Compliance with UL standards',
                        'Factory inspection',
                        'Follow-up services'
                    ],
                    'url': 'https://www.ul.com/services/product-certification'
                },
                'fcc': {
                    'name': 'FCC Certification',
                    'description': 'Certification for electromagnetic compatibility',
                    'requirements': [
                        'EMC testing',
                        'Compliance with FCC regulations',
                        'Technical documentation',
                        'FCC ID assignment'
                    ],
                    'url': 'https://www.fcc.gov/engineering-technology/laboratory-division/general/equipment-authorization'
                }
            },
            'packaging': {
                'sustainable_packaging_coalition': {
                    'name': 'How2Recycle Label',
                    'description': 'Standardized labeling system for recyclable packaging',
                    'requirements': [
                        'Packaging assessment',
                        'Compliance with recyclability criteria',
                        'Proper label usage',
                        'Annual membership'
                    ],
                    'url': 'https://how2recycle.info/'
                }
            },
            'fashion': {
                'oeko_tex': {
                    'name': 'OEKO-TEX Standard 100',
                    'description': 'Certification for textiles tested for harmful substances',
                    'requirements': [
                        'Product testing',
                        'Compliance with OEKO-TEX criteria',
                        'Documentation of test results',
                        'Annual recertification'
                    ],
                    'url': 'https://www.oeko-tex.com/en/our-standards/standard-100-by-oeko-tex'
                },
                'gots': {
                    'name': 'Global Organic Textile Standard (GOTS)',
                    'description': 'Certification for organic textiles',
                    'requirements': [
                        'Organic fiber content verification',
                        'Processing criteria compliance',
                        'Social criteria compliance',
                        'On-site inspection'
                    ],
                    'url': 'https://www.global-standard.org/'
                }
            }
        }
        
        logger.info("Initialized default compliance database")
    
    def save_database(self, output_path=None):
        """
        Save the compliance database to a file.
        
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
                    'regulations': self.regulations,
                    'compliance_rules': self.compliance_rules,
                    'certification_requirements': self.certification_requirements,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"Saved compliance database to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving compliance database: {str(e)}")
            return False
    
    def get_regulations_by_region(self, region, country=None):
        """
        Get regulations for a specific region and optionally country.
        
        Args:
            region (str): Region name (e.g., 'north_america', 'europe', 'asia')
            country (str, optional): Country name
            
        Returns:
            dict: Regulations for the specified region/country
        """
        if region not in self.regulations:
            return {}
        
        if country and country in self.regulations[region]:
            return self.regulations[region][country]
        elif not country:
            # Return all regulations for the region
            regulations = {}
            for country_code, country_regs in self.regulations[region].items():
                regulations.update(country_regs)
            return regulations
        
        return {}
    
    def get_global_regulations(self):
        """
        Get global regulations applicable to all regions.
        
        Returns:
            dict: Global regulations
        """
        return self.regulations.get('global', {})
    
    def get_compliance_rules_by_industry(self, industry, category=None):
        """
        Get compliance rules for a specific industry and optionally category.
        
        Args:
            industry (str): Industry name
            category (str, optional): Rule category (e.g., 'safety', 'materials')
            
        Returns:
            list: Compliance rules
        """
        if industry not in self.compliance_rules:
            return []
        
        if category and category in self.compliance_rules[industry]:
            return self.compliance_rules[industry][category]
        elif not category:
            # Return all rules for the industry
            rules = []
            for cat, cat_rules in self.compliance_rules[industry].items():
                rules.extend(cat_rules)
            return rules
        
        return []
    
    def get_certification_requirements_by_industry(self, industry):
        """
        Get certification requirements for a specific industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            dict: Certification requirements
        """
        return self.certification_requirements.get(industry, {})
    
    def check_product_compliance(self, product_data):
        """
        Check a product design for compliance with relevant regulations and standards.
        
        Args:
            product_data (dict): Product design data
            
        Returns:
            dict: Compliance check results
        """
        try:
            # Extract product information
            industry = product_data.get('industry', '')
            regions = product_data.get('target_regions', [])
            attributes = product_data.get('attributes', {})
            materials = product_data.get('materials', [])
            
            if not industry:
                return {
                    'product': product_data.get('name', 'Unknown'),
                    'compliance_status': 'Unknown',
                    'error': 'Industry not specified in product data'
                }
            
            # Get relevant compliance rules
            industry_rules = self.get_compliance_rules_by_industry(industry)
            
            # Get relevant regulations
            applicable_regulations = self.get_global_regulations()
            for region in regions:
                region_regs = self.get_regulations_by_region(region)
                applicable_regulations.update(region_regs)
            
            # Check compliance with rules
            rule_checks = []
            
            for rule in industry_rules:
                rule_result = self._check_rule_compliance(rule, attributes, materials)
                rule_checks.append(rule_result)
            
            # Check compliance with regulations
            regulation_checks = []
            
            for reg_id, regulation in applicable_regulations.items():
                reg_result = self._check_regulation_compliance(regulation, attributes, materials)
                regulation_checks.append(reg_result)
            
            # Calculate overall compliance status
            critical_failures = [r for r in rule_checks + regulation_checks if r['status'] == 'Non-Compliant' and r.get('severity') == 'Critical']
            high_failures = [r for r in rule_checks + regulation_checks if r['status'] == 'Non-Compliant' and r.get('severity') == 'High']
            medium_failures = [r for r in rule_checks + regulation_checks if r['status'] == 'Non-Compliant' and r.get('severity') == 'Medium']
            
            if critical_failures:
                compliance_status = 'Critical Non-Compliance'
            elif high_failures:
                compliance_status = 'Major Non-Compliance'
            elif medium_failures:
                compliance_status = 'Minor Non-Compliance'
            else:
                compliance_status = 'Compliant'
            
            # Generate recommendations
            recommendations = self._generate_compliance_recommendations(critical_failures + high_failures + medium_failures)
            
            # Create compliance report
            report = {
                'product': product_data.get('name', 'Unknown'),
                'industry': industry,
                'target_regions': regions,
                'compliance_status': compliance_status,
                'rule_checks': rule_checks,
                'regulation_checks': regulation_checks,
                'critical_issues': len(critical_failures),
                'high_issues': len(high_failures),
                'medium_issues': len(medium_failures),
                'recommendations': recommendations
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error checking product compliance: {str(e)}")
            return {
                'product': product_data.get('name', 'Unknown'),
                'compliance_status': 'Error',
                'error': str(e)
            }
    
    def _check_rule_compliance(self, rule, attributes, materials):
        """
        Check compliance with a specific rule.
        
        Args:
            rule (dict): Compliance rule
            attributes (dict): Product attributes
            materials (list): Product materials
            
        Returns:
            dict: Rule compliance result
        """
        # Initialize result
        result = {
            'rule': rule.get('name'),
            'description': rule.get('description'),
            'applicable_standards': rule.get('applicable_standards', []),
            'severity': rule.get('severity', 'Medium'),
            'status': 'Unknown',
            'details': []
        }
        
        # Check rule compliance based on rule type and product attributes
        rule_name = rule.get('name', '').lower()
        
        # Simulate compliance check based on rule name and attributes
        if 'stability' in rule_name:
            if 'stability_tested' in attributes and attributes['stability_tested']:
                result['status'] = 'Compliant'
                result['details'].append('Stability testing performed')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No stability testing documented')
        
        elif 'sharp edge' in rule_name:
            if 'edge_treatment' in attributes and attributes['edge_treatment']:
                result['status'] = 'Compliant'
                result['details'].append('Edge treatment applied')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No edge treatment specified')
        
        elif 'load capacity' in rule_name:
            if 'load_tested' in attributes and attributes['load_tested']:
                result['status'] = 'Compliant'
                result['details'].append('Load capacity testing performed')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No load capacity testing documented')
        
        elif 'formaldehyde' in rule_name:
            if 'formaldehyde_free' in attributes and attributes['formaldehyde_free']:
                result['status'] = 'Compliant'
                result['details'].append('Formaldehyde-free materials used')
            elif 'formaldehyde_level' in attributes and attributes['formaldehyde_level'] <= 0.05:
                result['status'] = 'Compliant'
                result['details'].append(f"Formaldehyde level ({attributes['formaldehyde_level']} ppm) within limits")
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Formaldehyde levels not specified or exceed limits')
        
        elif 'flame' in rule_name:
            if 'flame_retardant' in attributes and attributes['flame_retardant']:
                result['status'] = 'Compliant'
                result['details'].append('Flame retardant materials used')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No flame retardant properties specified')
        
        elif 'electrical safety' in rule_name:
            if 'electrical_safety_tested' in attributes and attributes['electrical_safety_tested']:
                result['status'] = 'Compliant'
                result['details'].append('Electrical safety testing performed')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No electrical safety testing documented')
        
        elif 'thermal' in rule_name:
            if 'thermal_safety_tested' in attributes and attributes['thermal_safety_tested']:
                result['status'] = 'Compliant'
                result['details'].append('Thermal safety testing performed')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No thermal safety testing documented')
        
        elif 'electromagnetic' in rule_name or 'emc' in rule_name:
            if 'emc_tested' in attributes and attributes['emc_tested']:
                result['status'] = 'Compliant'
                result['details'].append('EMC testing performed')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No EMC testing documented')
        
        elif 'hazardous substances' in rule_name or 'restricted substances' in rule_name:
            if 'rohs_compliant' in attributes and attributes['rohs_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('RoHS compliant materials used')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('RoHS compliance not specified')
        
        elif 'energy efficiency' in rule_name:
            if 'energy_efficient' in attributes and attributes['energy_efficient']:
                result['status'] = 'Compliant'
                result['details'].append('Energy efficiency requirements met')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Energy efficiency not specified')
        
        elif 'heavy metals' in rule_name:
            if 'heavy_metal_free' in attributes and attributes['heavy_metal_free']:
                result['status'] = 'Compliant'
                result['details'].append('Heavy metal free materials used')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Heavy metal content not specified')
        
        elif 'recyclability' in rule_name:
            if 'recyclable' in attributes and attributes['recyclable']:
                result['status'] = 'Compliant'
                result['details'].append('Recyclable materials used')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Recyclability not specified')
        
        elif 'azo dyes' in rule_name:
            if 'azo_free' in attributes and attributes['azo_free']:
                result['status'] = 'Compliant'
                result['details'].append('Azo-free dyes used')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Azo dye content not specified')
        
        elif 'flammability' in rule_name:
            if 'flammability_tested' in attributes and attributes['flammability_tested']:
                result['status'] = 'Compliant'
                result['details'].append('Flammability testing performed')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('No flammability testing documented')
        
        elif 'children' in rule_name:
            if 'child_safety_compliant' in attributes and attributes['child_safety_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('Child safety requirements met')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Child safety compliance not specified')
        
        elif 'fiber content' in rule_name:
            if 'fiber_content_labeled' in attributes and attributes['fiber_content_labeled']:
                result['status'] = 'Compliant'
                result['details'].append('Fiber content labeling requirements met')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Fiber content labeling not specified')
        
        elif 'care instructions' in rule_name:
            if 'care_instructions_included' in attributes and attributes['care_instructions_included']:
                result['status'] = 'Compliant'
                result['details'].append('Care instructions included')
            else:
                result['status'] = 'Non-Compliant'
                result['details'].append('Care instructions not specified')
        
        else:
            # Default to "Needs Review" for rules that can't be automatically checked
            result['status'] = 'Needs Review'
            result['details'].append('Manual review required')
        
        return result
    
    def _check_regulation_compliance(self, regulation, attributes, materials):
        """
        Check compliance with a specific regulation.
        
        Args:
            regulation (dict): Regulation data
            attributes (dict): Product attributes
            materials (list): Product materials
            
        Returns:
            dict: Regulation compliance result
        """
        # Initialize result
        result = {
            'regulation': regulation.get('name'),
            'description': regulation.get('description'),
            'scope': regulation.get('scope'),
            'status': 'Unknown',
            'details': []
        }
        
        # Check regulation compliance based on regulation name and attributes
        reg_name = regulation.get('name', '').lower()
        
        # Simulate compliance check based on regulation name and attributes
        if 'iso 9001' in reg_name:
            if 'iso_9001_certified' in attributes and attributes['iso_9001_certified']:
                result['status'] = 'Compliant'
                result['details'].append('ISO 9001 certification documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('ISO 9001 certification status not specified')
        
        elif 'iso 14001' in reg_name:
            if 'iso_14001_certified' in attributes and attributes['iso_14001_certified']:
                result['status'] = 'Compliant'
                result['details'].append('ISO 14001 certification documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('ISO 14001 certification status not specified')
        
        elif 'cpsc' in reg_name:
            if 'cpsc_compliant' in attributes and attributes['cpsc_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('CPSC compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('CPSC compliance status not specified')
        
        elif 'fda' in reg_name:
            if 'fda_compliant' in attributes and attributes['fda_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('FDA compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('FDA compliance status not specified')
        
        elif 'fcc' in reg_name:
            if 'fcc_compliant' in attributes and attributes['fcc_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('FCC compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('FCC compliance status not specified')
        
        elif 'health canada' in reg_name:
            if 'health_canada_compliant' in attributes and attributes['health_canada_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('Health Canada compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('Health Canada compliance status not specified')
        
        elif 'ce marking' in reg_name:
            if 'ce_marked' in attributes and attributes['ce_marked']:
                result['status'] = 'Compliant'
                result['details'].append('CE marking documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('CE marking status not specified')
        
        elif 'rohs' in reg_name:
            if 'rohs_compliant' in attributes and attributes['rohs_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('RoHS compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('RoHS compliance status not specified')
        
        elif 'reach' in reg_name:
            if 'reach_compliant' in attributes and attributes['reach_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('REACH compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('REACH compliance status not specified')
        
        elif 'weee' in reg_name:
            if 'weee_compliant' in attributes and attributes['weee_compliant']:
                result['status'] = 'Compliant'
                result['details'].append('WEEE compliance documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('WEEE compliance status not specified')
        
        elif 'ccc' in reg_name:
            if 'ccc_certified' in attributes and attributes['ccc_certified']:
                result['status'] = 'Compliant'
                result['details'].append('CCC certification documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('CCC certification status not specified')
        
        elif 'pse' in reg_name:
            if 'pse_certified' in attributes and attributes['pse_certified']:
                result['status'] = 'Compliant'
                result['details'].append('PSE certification documented')
            else:
                result['status'] = 'Needs Review'
                result['details'].append('PSE certification status not specified')
        
        else:
            # Default to "Needs Review" for regulations that can't be automatically checked
            result['status'] = 'Needs Review'
            result['details'].append('Manual review required')
        
        # Determine severity based on status
        if result['status'] == 'Non-Compliant':
            result['severity'] = 'High'
        elif result['status'] == 'Needs Review':
            result['severity'] = 'Medium'
        else:
            result['severity'] = 'Low'
        
        return result
    
    def _generate_compliance_recommendations(self, non_compliant_checks):
        """
        Generate recommendations to address non-compliance issues.
        
        Args:
            non_compliant_checks (list): Non-compliant check results
            
        Returns:
            list: Compliance recommendations
        """
        recommendations = []
        
        for check in non_compliant_checks:
            rule_name = check.get('rule') or check.get('regulation', '')
            
            # Generate recommendation based on rule/regulation name
            if 'stability' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Conduct stability testing according to applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'sharp edge' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Apply edge treatments to eliminate sharp edges and corners',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'load capacity' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Conduct load capacity testing according to applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'formaldehyde' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Use formaldehyde-free materials or ensure levels are below regulatory limits',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'flame' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Use flame retardant materials or treatments that meet applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'electrical safety' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Conduct electrical safety testing according to applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'thermal' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Conduct thermal safety testing according to applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'electromagnetic' in rule_name.lower() or 'emc' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Conduct EMC testing according to applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'hazardous substances' in rule_name.lower() or 'restricted substances' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure materials comply with RoHS and other hazardous substance regulations',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'energy efficiency' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Improve energy efficiency to meet applicable standards',
                    'priority': 'Medium'
                })
            
            elif 'heavy metals' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Use materials free of restricted heavy metals',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'recyclability' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Use recyclable materials and include appropriate recycling markings',
                    'priority': 'Medium'
                })
            
            elif 'azo dyes' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Use azo-free dyes that comply with applicable regulations',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'flammability' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Conduct flammability testing according to applicable standards',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'children' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure design meets all child safety requirements',
                    'priority': 'High' if check.get('severity') == 'Critical' else 'Medium'
                })
            
            elif 'fiber content' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Include accurate fiber content labeling',
                    'priority': 'Medium'
                })
            
            elif 'care instructions' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Include appropriate care instructions',
                    'priority': 'Medium'
                })
            
            elif 'iso 9001' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Implement ISO 9001 quality management system',
                    'priority': 'Medium'
                })
            
            elif 'iso 14001' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Implement ISO 14001 environmental management system',
                    'priority': 'Medium'
                })
            
            elif 'cpsc' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure compliance with CPSC regulations',
                    'priority': 'High'
                })
            
            elif 'fda' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure compliance with FDA regulations',
                    'priority': 'High'
                })
            
            elif 'fcc' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure compliance with FCC regulations',
                    'priority': 'High'
                })
            
            elif 'health canada' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure compliance with Health Canada regulations',
                    'priority': 'High'
                })
            
            elif 'ce marking' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Complete CE marking process including technical documentation and conformity assessment',
                    'priority': 'High'
                })
            
            elif 'rohs' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure materials comply with RoHS directive',
                    'priority': 'High'
                })
            
            elif 'reach' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure materials comply with REACH regulation',
                    'priority': 'High'
                })
            
            elif 'weee' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Ensure compliance with WEEE directive',
                    'priority': 'Medium'
                })
            
            elif 'ccc' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Obtain CCC certification for products sold in China',
                    'priority': 'High'
                })
            
            elif 'pse' in rule_name.lower():
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Obtain PSE certification for electrical products sold in Japan',
                    'priority': 'High'
                })
            
            else:
                # Generic recommendation for other issues
                recommendations.append({
                    'issue': rule_name,
                    'recommendation': 'Review and address compliance requirements',
                    'priority': 'Medium'
                })
        
        # Remove duplicates
        unique_recommendations = []
        seen_issues = set()
        
        for rec in recommendations:
            if rec['issue'] not in seen_issues:
                unique_recommendations.append(rec)
                seen_issues.add(rec['issue'])
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        unique_recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return unique_recommendations
    
    def get_certification_path(self, product_data):
        """
        Get certification path for a product based on its attributes.
        
        Args:
            product_data (dict): Product design data
            
        Returns:
            dict: Certification path information
        """
        try:
            # Extract product information
            industry = product_data.get('industry', '')
            regions = product_data.get('target_regions', [])
            attributes = product_data.get('attributes', {})
            
            if not industry:
                return {
                    'product': product_data.get('name', 'Unknown'),
                    'error': 'Industry not specified in product data'
                }
            
            # Get relevant certification requirements
            industry_certifications = self.get_certification_requirements_by_industry(industry)
            
            # Determine applicable certifications
            applicable_certifications = []
            
            for cert_id, cert_data in industry_certifications.items():
                # Check if certification is relevant based on product attributes
                is_applicable = self._is_certification_applicable(cert_id, cert_data, attributes, regions)
                
                if is_applicable:
                    applicable_certifications.append({
                        'id': cert_id,
                        'name': cert_data.get('name'),
                        'description': cert_data.get('description'),
                        'requirements': cert_data.get('requirements', []),
                        'url': cert_data.get('url')
                    })
            
            # Create certification path
            certification_path = {
                'product': product_data.get('name', 'Unknown'),
                'industry': industry,
                'target_regions': regions,
                'recommended_certifications': applicable_certifications,
                'certification_steps': self._generate_certification_steps(applicable_certifications)
            }
            
            return certification_path
            
        except Exception as e:
            logger.error(f"Error generating certification path: {str(e)}")
            return {
                'product': product_data.get('name', 'Unknown'),
                'error': str(e)
            }
    
    def _is_certification_applicable(self, cert_id, cert_data, attributes, regions):
        """
        Determine if a certification is applicable to a product.
        
        Args:
            cert_id (str): Certification identifier
            cert_data (dict): Certification data
            attributes (dict): Product attributes
            regions (list): Target regions
            
        Returns:
            bool: True if certification is applicable, False otherwise
        """
        # Check certification applicability based on attributes and regions
        if cert_id == 'ansi_bifma':
            # Applicable for commercial furniture
            return 'commercial' in attributes.get('market_segment', '').lower()
        
        elif cert_id == 'greenguard':
            # Applicable for indoor products
            return attributes.get('indoor_use', False)
        
        elif cert_id == 'fsc':
            # Applicable for products containing wood
            return 'wood' in attributes.get('materials', [])
        
        elif cert_id == 'energy_star':
            # Applicable for energy-consuming products in North America
            return attributes.get('energy_consuming', False) and any(r.lower() in ['north_america', 'usa', 'canada'] for r in regions)
        
        elif cert_id == 'ul':
            # Applicable for electrical products
            return attributes.get('electrical', False)
        
        elif cert_id == 'fcc':
            # Applicable for electronic products in North America
            return attributes.get('electronic', False) and any(r.lower() in ['north_america', 'usa'] for r in regions)
        
        elif cert_id == 'sustainable_packaging_coalition':
            # Applicable for packaging products
            return 'packaging' in attributes.get('product_type', '').lower()
        
        elif cert_id == 'oeko_tex':
            # Applicable for textile products
            return 'textile' in attributes.get('materials', [])
        
        elif cert_id == 'gots':
            # Applicable for organic textile products
            return 'textile' in attributes.get('materials', []) and attributes.get('organic', False)
        
        # Default to True for unknown certifications
        return True
    
    def _generate_certification_steps(self, certifications):
        """
        Generate certification steps for applicable certifications.
        
        Args:
            certifications (list): Applicable certifications
            
        Returns:
            list: Certification steps
        """
        steps = []
        
        for i, cert in enumerate(certifications):
            step = {
                'step': i + 1,
                'certification': cert['name'],
                'actions': []
            }
            
            # Add actions based on certification requirements
            for req in cert.get('requirements', []):
                step['actions'].append({
                    'description': req,
                    'status': 'Pending'
                })
            
            steps.append(step)
        
        return steps
    
    def add_regulation(self, region, country, reg_id, reg_data):
        """
        Add a new regulation to the database.
        
        Args:
            region (str): Region name
            country (str): Country name
            reg_id (str): Regulation identifier
            reg_data (dict): Regulation information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate regulation data
            required_fields = ['name', 'description', 'scope']
            for field in required_fields:
                if field not in reg_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add regulation to database
            if region not in self.regulations:
                self.regulations[region] = {}
            
            if country not in self.regulations[region]:
                self.regulations[region][country] = {}
            
            self.regulations[region][country][reg_id] = reg_data
            logger.info(f"Added regulation: {reg_id} for {region}/{country}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding regulation: {str(e)}")
            return False
    
    def add_compliance_rule(self, industry, category, rule_data):
        """
        Add a new compliance rule to the database.
        
        Args:
            industry (str): Industry name
            category (str): Rule category
            rule_data (dict): Rule information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate rule data
            required_fields = ['name', 'description']
            for field in required_fields:
                if field not in rule_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add rule to database
            if industry not in self.compliance_rules:
                self.compliance_rules[industry] = {}
            
            if category not in self.compliance_rules[industry]:
                self.compliance_rules[industry][category] = []
            
            self.compliance_rules[industry][category].append(rule_data)
            logger.info(f"Added compliance rule: {rule_data['name']} for {industry}/{category}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding compliance rule: {str(e)}")
            return False
    
    def add_certification_requirement(self, industry, cert_id, cert_data):
        """
        Add a new certification requirement to the database.
        
        Args:
            industry (str): Industry name
            cert_id (str): Certification identifier
            cert_data (dict): Certification information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate certification data
            required_fields = ['name', 'description', 'requirements']
            for field in required_fields:
                if field not in cert_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add certification to database
            if industry not in self.certification_requirements:
                self.certification_requirements[industry] = {}
            
            self.certification_requirements[industry][cert_id] = cert_data
            logger.info(f"Added certification requirement: {cert_id} for {industry}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding certification requirement: {str(e)}")
            return False


if __name__ == "__main__":
    # Example usage
    checker = ComplianceChecker()
    
    # Get regulations by region
    eu_regulations = checker.get_regulations_by_region('europe', 'eu')
    print(f"Found {len(eu_regulations)} EU regulations")
    
    # Get compliance rules by industry
    furniture_rules = checker.get_compliance_rules_by_industry('furniture')
    print(f"Found {len(furniture_rules)} furniture compliance rules")
    
    # Check product compliance
    product_data = {
        'name': 'Office Chair',
        'industry': 'furniture',
        'target_regions': ['north_america', 'europe'],
        'attributes': {
            'stability_tested': True,
            'edge_treatment': True,
            'load_tested': True,
            'formaldehyde_free': True,
            'flame_retardant': True,
            'market_segment': 'Commercial'
        },
        'materials': ['steel', 'polyester', 'nylon']
    }
    
    compliance_report = checker.check_product_compliance(product_data)
    print(f"Product compliance status: {compliance_report['compliance_status']}")
    
    # Get certification path
    certification_path = checker.get_certification_path(product_data)
    print(f"Recommended certifications: {len(certification_path['recommended_certifications'])}")
