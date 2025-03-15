import logging
import json
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IndustryStandards:
    """
    Class for managing industry standards and regulations across various industries.
    Provides information about compliance requirements and design guidelines.
    """
    
    def __init__(self, standards_path=None):
        """
        Initialize the IndustryStandards.
        
        Args:
            standards_path (str, optional): Path to the standards database file
        """
        logger.info("Initializing IndustryStandards")
        self.standards_path = standards_path
        self.standards = {}
        self.industries = {}
        self._load_standards()
    
    def _load_standards(self):
        """
        Load standards from database file or initialize with default standards.
        """
        try:
            if self.standards_path and os.path.exists(self.standards_path):
                with open(self.standards_path, 'r') as f:
                    data = json.load(f)
                    self.standards = data.get('standards', {})
                    self.industries = data.get('industries', {})
                logger.info(f"Loaded {len(self.standards)} standards from database")
            else:
                logger.info("Initializing default standards database")
                self._initialize_default_standards()
        except Exception as e:
            logger.error(f"Error loading standards: {str(e)}")
            self._initialize_default_standards()
    
    def _initialize_default_standards(self):
        """
        Initialize the database with default industry standards and regulations.
        """
        # Define industry categories
        self.industries = {
            'furniture': {
                'description': 'Standards for furniture design, manufacturing, and safety',
                'subcategories': ['residential', 'office', 'outdoor', 'children']
            },
            'electronics': {
                'description': 'Standards for electronic devices and components',
                'subcategories': ['consumer', 'industrial', 'medical', 'telecommunications']
            },
            'packaging': {
                'description': 'Standards for packaging materials, design, and labeling',
                'subcategories': ['food', 'retail', 'industrial', 'shipping']
            },
            'fashion': {
                'description': 'Standards for apparel, accessories, and textiles',
                'subcategories': ['apparel', 'footwear', 'accessories', 'textiles']
            },
            'home_goods': {
                'description': 'Standards for household products and appliances',
                'subcategories': ['kitchenware', 'bathroom', 'decorative', 'appliances']
            },
            'medical': {
                'description': 'Standards for medical devices and healthcare products',
                'subcategories': ['devices', 'equipment', 'supplies', 'wearables']
            },
            'construction': {
                'description': 'Standards for building materials and construction products',
                'subcategories': ['structural', 'finishes', 'electrical', 'plumbing']
            },
            'automotive': {
                'description': 'Standards for automotive components and accessories',
                'subcategories': ['interior', 'exterior', 'electronics', 'accessories']
            }
        }
        
        # Initialize default standards
        self.standards = {
            # Furniture Standards
            'ansi_bifma_x5_1': {
                'id': 'ANSI/BIFMA X5.1',
                'name': 'Office Chairs',
                'industry': 'furniture',
                'subcategory': 'office',
                'description': 'Safety and performance requirements for office chairs',
                'key_requirements': [
                    'Stability testing under various load conditions',
                    'Durability testing for cyclic loading',
                    'Structural integrity testing',
                    'Drop testing for impact resistance'
                ],
                'compliance_criteria': {
                    'stability': 'Chair must not tip over when tested according to specified methods',
                    'durability': 'Chair must withstand 100,000 cycles of loading without failure',
                    'structural_integrity': 'No structural failure when loaded to 300 lbs',
                    'impact_resistance': 'No structural failure after drop tests'
                },
                'testing_methods': [
                    'Front stability test',
                    'Rear stability test',
                    'Arm strength test',
                    'Backrest durability test',
                    'Seat durability test'
                ],
                'region': 'North America',
                'mandatory': False,
                'last_updated': '2022-01-15'
            },
            'cal_tb_117': {
                'id': 'CAL TB 117-2013',
                'name': 'Flammability of Upholstered Furniture',
                'industry': 'furniture',
                'subcategory': 'residential',
                'description': 'Requirements for fire retardant properties of upholstered furniture',
                'key_requirements': [
                    'Smolder resistance of cover fabrics',
                    'Smolder resistance of barrier materials',
                    'Smolder resistance of resilient filling materials',
                    'Open flame resistance testing'
                ],
                'compliance_criteria': {
                    'smolder_resistance': 'Char length must not exceed 1.8 inches',
                    'open_flame': 'No ignition or progressive combustion after 12-second flame application'
                },
                'testing_methods': [
                    'Cigarette ignition test',
                    'Small open flame test'
                ],
                'region': 'California, USA',
                'mandatory': True,
                'last_updated': '2013-06-01'
            },
            'astm_f2057': {
                'id': 'ASTM F2057',
                'name': 'Safety of Clothing Storage Units',
                'industry': 'furniture',
                'subcategory': 'residential',
                'description': 'Stability requirements for clothing storage units to prevent tip-over',
                'key_requirements': [
                    'Stability testing with all drawers open',
                    'Stability testing with load applied to open drawer',
                    'Warning label requirements',
                    'Tip restraint inclusion'
                ],
                'compliance_criteria': {
                    'stability': 'Unit must not tip over when all drawers are open and loaded',
                    'tip_restraint': 'Must include tip restraint device and installation instructions',
                    'warning_label': 'Must include permanent warning label about tip-over hazard'
                },
                'testing_methods': [
                    'Empty stability test',
                    'Loaded stability test',
                    'Interlock system test (if applicable)'
                ],
                'region': 'United States',
                'mandatory': False,
                'last_updated': '2019-08-01'
            },
            
            # Electronics Standards
            'iec_60950': {
                'id': 'IEC 60950-1',
                'name': 'Information Technology Equipment Safety',
                'industry': 'electronics',
                'subcategory': 'consumer',
                'description': 'Safety requirements for information technology equipment',
                'key_requirements': [
                    'Electric shock protection',
                    'Energy hazards protection',
                    'Fire enclosure requirements',
                    'Mechanical strength requirements',
                    'Temperature limits'
                ],
                'compliance_criteria': {
                    'electric_shock': 'No access to hazardous voltage parts',
                    'fire_enclosure': 'Fire must be contained within equipment',
                    'temperature': 'Surface temperatures must not exceed specified limits'
                },
                'testing_methods': [
                    'Electric strength test',
                    'Leakage current test',
                    'Abnormal operation test',
                    'Temperature rise test'
                ],
                'region': 'International',
                'mandatory': True,
                'last_updated': '2018-05-20'
            },
            'energy_star': {
                'id': 'ENERGY STAR',
                'name': 'Energy Efficiency for Electronics',
                'industry': 'electronics',
                'subcategory': 'consumer',
                'description': 'Energy efficiency requirements for consumer electronics',
                'key_requirements': [
                    'Power consumption limits in active mode',
                    'Power consumption limits in standby mode',
                    'Power management features',
                    'Energy efficiency metrics'
                ],
                'compliance_criteria': {
                    'active_power': 'Must not exceed specified limits for product category',
                    'standby_power': 'Must not exceed 0.5W in standby mode',
                    'power_management': 'Must include automatic power-down features'
                },
                'testing_methods': [
                    'Power consumption measurement in various modes',
                    'Efficiency calculation methods'
                ],
                'region': 'United States',
                'mandatory': False,
                'last_updated': '2023-01-10'
            },
            'rohs': {
                'id': 'RoHS 3',
                'name': 'Restriction of Hazardous Substances',
                'industry': 'electronics',
                'subcategory': 'all',
                'description': 'Restrictions on the use of hazardous substances in electrical and electronic equipment',
                'key_requirements': [
                    'Lead (Pb) < 0.1%',
                    'Mercury (Hg) < 0.1%',
                    'Cadmium (Cd) < 0.01%',
                    'Hexavalent chromium (Cr6+) < 0.1%',
                    'Polybrominated biphenyls (PBB) < 0.1%',
                    'Polybrominated diphenyl ethers (PBDE) < 0.1%',
                    'Bis(2-ethylhexyl) phthalate (DEHP) < 0.1%',
                    'Butyl benzyl phthalate (BBP) < 0.1%',
                    'Dibutyl phthalate (DBP) < 0.1%',
                    'Diisobutyl phthalate (DIBP) < 0.1%'
                ],
                'compliance_criteria': {
                    'substance_limits': 'Concentration of restricted substances must be below specified limits',
                    'documentation': 'Technical documentation must be maintained for compliance verification'
                },
                'testing_methods': [
                    'X-ray fluorescence (XRF) screening',
                    'Inductively coupled plasma (ICP) analysis',
                    'Gas chromatography-mass spectrometry (GC-MS)'
                ],
                'region': 'European Union',
                'mandatory': True,
                'last_updated': '2019-07-22'
            },
            
            # Packaging Standards
            'iso_3394': {
                'id': 'ISO 3394',
                'name': 'Packaging Dimensions',
                'industry': 'packaging',
                'subcategory': 'shipping',
                'description': 'Dimensional standards for transport packages and unit loads',
                'key_requirements': [
                    'Standard base dimensions of 600 x 400 mm',
                    'Modular system for package sizes',
                    'Height recommendations',
                    'Stacking considerations'
                ],
                'compliance_criteria': {
                    'dimensions': 'Package dimensions must be modular multiples or fractions of 600 x 400 mm',
                    'tolerances': 'Dimensional tolerances must be within specified limits'
                },
                'testing_methods': [
                    'Dimensional measurement',
                    'Stacking performance testing'
                ],
                'region': 'International',
                'mandatory': False,
                'last_updated': '2012-09-15'
            },
            'astm_d4169': {
                'id': 'ASTM D4169',
                'name': 'Performance Testing of Shipping Containers',
                'industry': 'packaging',
                'subcategory': 'shipping',
                'description': 'Standard practice for performance testing of shipping containers and systems',
                'key_requirements': [
                    'Atmospheric conditioning',
                    'Handling drop tests',
                    'Stacking test',
                    'Vibration test',
                    'Impact test'
                ],
                'compliance_criteria': {
                    'integrity': 'Package must maintain physical integrity after testing',
                    'product_protection': 'Contents must be undamaged after testing sequence'
                },
                'testing_methods': [
                    'Drop test from specified heights',
                    'Compression test with specified load',
                    'Vibration test with specified profile',
                    'Impact test with specified energy'
                ],
                'region': 'United States',
                'mandatory': False,
                'last_updated': '2016-11-01'
            },
            
            # Fashion Standards
            'oeko_tex_100': {
                'id': 'OEKO-TEX Standard 100',
                'name': 'Textile Product Safety',
                'industry': 'fashion',
                'subcategory': 'textiles',
                'description': 'Testing and certification system for textile raw materials, intermediate and end products',
                'key_requirements': [
                    'Testing for harmful substances',
                    'pH value requirements',
                    'Formaldehyde limits',
                    'Heavy metal limits',
                    'Pesticide limits'
                ],
                'compliance_criteria': {
                    'harmful_substances': 'Concentration of harmful substances must be below specified limits',
                    'ph_value': 'pH value must be between 4.0 and 7.5',
                    'formaldehyde': 'Formaldehyde content must be below specified limits'
                },
                'testing_methods': [
                    'Chemical analysis for harmful substances',
                    'pH measurement',
                    'Formaldehyde content determination',
                    'Color fastness testing'
                ],
                'region': 'International',
                'mandatory': False,
                'last_updated': '2023-01-01'
            },
            'astm_d5489': {
                'id': 'ASTM D5489',
                'name': 'Care Labeling of Textiles',
                'industry': 'fashion',
                'subcategory': 'apparel',
                'description': 'Standard guide for care symbols for care instructions on textile products',
                'key_requirements': [
                    'Washing symbols',
                    'Bleaching symbols',
                    'Drying symbols',
                    'Ironing symbols',
                    'Professional textile care symbols'
                ],
                'compliance_criteria': {
                    'symbol_usage': 'Symbols must be used according to standard definitions',
                    'label_permanence': 'Care labels must remain legible for the useful life of the product'
                },
                'testing_methods': [
                    'Label durability testing',
                    'Verification of symbol accuracy'
                ],
                'region': 'United States',
                'mandatory': False,
                'last_updated': '2018-06-01'
            },
            
            # Home Goods Standards
            'ul_1026': {
                'id': 'UL 1026',
                'name': 'Electric Household Cooking Equipment',
                'industry': 'home_goods',
                'subcategory': 'appliances',
                'description': 'Safety standard for electric household cooking equipment',
                'key_requirements': [
                    'Electric shock protection',
                    'Thermal protection',
                    'Fire hazard prevention',
                    'Mechanical hazard prevention',
                    'Marking and instructions'
                ],
                'compliance_criteria': {
                    'electric_shock': 'No access to live parts',
                    'temperature': 'Surface temperatures must not exceed specified limits',
                    'fire_hazard': 'No ignition of surrounding materials under abnormal conditions'
                },
                'testing_methods': [
                    'Dielectric voltage-withstand test',
                    'Temperature test',
                    'Abnormal operation test',
                    'Strain relief test'
                ],
                'region': 'United States',
                'mandatory': True,
                'last_updated': '2020-03-15'
            },
            
            # Medical Standards
            'iso_13485': {
                'id': 'ISO 13485',
                'name': 'Medical Devices Quality Management',
                'industry': 'medical',
                'subcategory': 'all',
                'description': 'Quality management system requirements for medical devices',
                'key_requirements': [
                    'Quality management system',
                    'Management responsibility',
                    'Resource management',
                    'Product realization',
                    'Measurement, analysis and improvement'
                ],
                'compliance_criteria': {
                    'documentation': 'Comprehensive quality management system documentation',
                    'risk_management': 'Risk management throughout product lifecycle',
                    'traceability': 'Traceability of products and components'
                },
                'testing_methods': [
                    'Quality system audit',
                    'Process validation',
                    'Design verification and validation'
                ],
                'region': 'International',
                'mandatory': True,
                'last_updated': '2016-03-01'
            },
            
            # Construction Standards
            'astm_e84': {
                'id': 'ASTM E84',
                'name': 'Surface Burning Characteristics',
                'industry': 'construction',
                'subcategory': 'finishes',
                'description': 'Standard test method for surface burning characteristics of building materials',
                'key_requirements': [
                    'Flame spread index',
                    'Smoke developed index',
                    'Testing of representative samples',
                    'Classification of materials'
                ],
                'compliance_criteria': {
                    'flame_spread': 'Flame spread index must be within specified limits for intended use',
                    'smoke_developed': 'Smoke developed index must be within specified limits for intended use'
                },
                'testing_methods': [
                    'Tunnel test with standardized fire exposure',
                    'Measurement of flame spread distance',
                    'Measurement of smoke density'
                ],
                'region': 'United States',
                'mandatory': True,
                'last_updated': '2021-05-01'
            },
            
            # Automotive Standards
            'fmvss_302': {
                'id': 'FMVSS 302',
                'name': 'Flammability of Interior Materials',
                'industry': 'automotive',
                'subcategory': 'interior',
                'description': 'Flammability requirements for materials used in the occupant compartments of motor vehicles',
                'key_requirements': [
                    'Burn rate limits for interior materials',
                    'Testing of representative samples',
                    'Documentation of compliance'
                ],
                'compliance_criteria': {
                    'burn_rate': 'Burn rate must not exceed 102 mm per minute',
                    'self_extinguishing': 'Material must self-extinguish before burning 51 mm'
                },
                'testing_methods': [
                    'Horizontal burn rate test',
                    'Measurement of burn rate and distance'
                ],
                'region': 'United States',
                'mandatory': True,
                'last_updated': '2013-10-01'
            }
        }
        
        logger.info(f"Initialized default standards database with {len(self.standards)} standards")
    
    def save_database(self, output_path=None):
        """
        Save the standards database to a file.
        
        Args:
            output_path (str, optional): Path to save the database file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            path = output_path or self.standards_path
            if not path:
                logger.warning("No output path specified for saving database")
                return False
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Save database to file
            with open(path, 'w') as f:
                json.dump({
                    'standards': self.standards,
                    'industries': self.industries,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"Saved standards database to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving standards database: {str(e)}")
            return False
    
    def get_standard(self, standard_id):
        """
        Get information about a specific standard.
        
        Args:
            standard_id (str): Standard identifier
            
        Returns:
            dict: Standard information
        """
        return self.standards.get(standard_id, None)
    
    def get_standards_by_industry(self, industry, subcategory=None):
        """
        Get all standards for a specific industry and optional subcategory.
        
        Args:
            industry (str): Industry name
            subcategory (str, optional): Industry subcategory
            
        Returns:
            dict: Standards for the industry
        """
        if subcategory:
            return {k: v for k, v in self.standards.items() 
                   if v.get('industry') == industry and v.get('subcategory') == subcategory}
        else:
            return {k: v for k, v in self.standards.items() 
                   if v.get('industry') == industry}
    
    def get_mandatory_standards(self, industry, region=None):
        """
        Get mandatory standards for a specific industry and optional region.
        
        Args:
            industry (str): Industry name
            region (str, optional): Geographic region
            
        Returns:
            dict: Mandatory standards
        """
        if region:
            return {k: v for k, v in self.standards.items() 
                   if v.get('industry') == industry and v.get('mandatory', False) and v.get('region') == region}
        else:
            return {k: v for k, v in self.standards.items() 
                   if v.get('industry') == industry and v.get('mandatory', False)}
    
    def check_compliance(self, product_data, standard_id):
        """
        Check if a product complies with a specific standard.
        
        Args:
            product_data (dict): Product information
            standard_id (str): Standard identifier
            
        Returns:
            dict: Compliance check results
        """
        standard = self.get_standard(standard_id)
        if not standard:
            return {
                'compliant': False,
                'standard': standard_id,
                'reason': 'Standard not found'
            }
        
        # Initialize compliance check
        compliance_check = {
            'compliant': True,
            'standard': standard.get('id'),
            'standard_name': standard.get('name'),
            'checks': [],
            'missing_data': []
        }
        
        # Get compliance criteria
        criteria = standard.get('compliance_criteria', {})
        
        # Check each criterion
        for criterion_name, criterion_desc in criteria.items():
            # Check if product data contains necessary information
            if criterion_name not in product_data:
                compliance_check['missing_data'].append(criterion_name)
                compliance_check['compliant'] = False
                continue
            
            # Get product value and expected value/range
            product_value = product_data[criterion_name]
            
            # Perform compliance check based on criterion type
            check_result = self._check_criterion(criterion_name, product_value, criterion_desc, standard)
            
            # Add check result
            compliance_check['checks'].append(check_result)
            
            # Update overall compliance
            if not check_result['compliant']:
                compliance_check['compliant'] = False
        
        return compliance_check
    
    def _check_criterion(self, criterion_name, product_value, criterion_desc, standard):
        """
        Check a specific compliance criterion.
        
        Args:
            criterion_name (str): Name of the criterion
            product_value: Product's value for the criterion
            criterion_desc (str): Description of the criterion
            standard (dict): Standard information
            
        Returns:
            dict: Check result
        """
        # Initialize check result
        check_result = {
            'criterion': criterion_name,
            'description': criterion_desc,
            'product_value': product_value,
            'compliant': False,
            'details': ''
        }
        
        # Parse criterion description to determine expected values
        if 'must not exceed' in criterion_desc.lower():
            # Extract maximum value
            max_value = self._extract_numeric_value(criterion_desc)
            if max_value is not None:
                check_result['expected_value'] = f'<= {max_value}'
                check_result['compliant'] = product_value <= max_value
                check_result['details'] = f'Value {"is" if check_result["compliant"] else "is not"} within limit'
        
        elif 'must be between' in criterion_desc.lower():
            # Extract range values
            range_values = self._extract_range_values(criterion_desc)
            if range_values:
                min_value, max_value = range_values
                check_result['expected_value'] = f'{min_value} - {max_value}'
                check_result['compliant'] = min_value <= product_value <= max_value
                check_result['details'] = f'Value {"is" if check_result["compliant"] else "is not"} within range'
        
        elif 'must be below' in criterion_desc.lower():
            # Extract maximum value
            max_value = self._extract_numeric_value(criterion_desc)
            if max_value is not None:
                check_result['expected_value'] = f'< {max_value}'
                check_result['compliant'] = product_value < max_value
                check_result['details'] = f'Value {"is" if check_result["compliant"] else "is not"} below limit'
        
        elif 'must be above' in criterion_desc.lower():
            # Extract minimum value
            min_value = self._extract_numeric_value(criterion_desc)
            if min_value is not None:
                check_result['expected_value'] = f'> {min_value}'
                check_result['compliant'] = product_value > min_value
                check_result['details'] = f'Value {"is" if check_result["compliant"] else "is not"} above limit'
        
        else:
            # Boolean or string comparison
            if isinstance(product_value, bool):
                expected_value = 'true' in criterion_desc.lower() or 'must include' in criterion_desc.lower()
                check_result['expected_value'] = expected_value
                check_result['compliant'] = product_value == expected_value
                check_result['details'] = f'Value {"matches" if check_result["compliant"] else "does not match"} requirement'
            elif isinstance(product_value, str):
                # Check if product value contains any of the required terms
                required_terms = self._extract_required_terms(criterion_desc)
                if required_terms:
                    check_result['expected_value'] = required_terms
                    check_result['compliant'] = any(term.lower() in product_value.lower() for term in required_terms)
                    check_result['details'] = f'Value {"contains" if check_result["compliant"] else "does not contain"} required terms'
        
        return check_result
    
    def _extract_numeric_value(self, text):
        """
        Extract a numeric value from text.
        
        Args:
            text (str): Text containing a numeric value
            
        Returns:
            float: Extracted numeric value, or None if not found
        """
        import re
        
        # Find numeric values in text
        matches = re.findall(r'(\d+(?:\.\d+)?)', text)
        if matches:
            return float(matches[0])
        return None
    
    def _extract_range_values(self, text):
        """
        Extract range values from text.
        
        Args:
            text (str): Text containing range values
            
        Returns:
            tuple: (min_value, max_value), or None if not found
        """
        import re
        
        # Find range values in text (e.g., "between 4.0 and 7.5")
        matches = re.findall(r'between\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)', text)
        if matches:
            return float(matches[0][0]), float(matches[0][1])
        return None
    
    def _extract_required_terms(self, text):
        """
        Extract required terms from text.
        
        Args:
            text (str): Text containing required terms
            
        Returns:
            list: Required terms
        """
        import re
        
        # Find required terms in text (e.g., "must include X, Y, Z")
        matches = re.findall(r'must include\s+([\w\s,]+)', text)
        if matches:
            terms = matches[0].split(',')
            return [term.strip() for term in terms]
        return []
    
    def get_compliance_requirements(self, industry, product_type, region=None):
        """
        Get compliance requirements for a specific product type.
        
        Args:
            industry (str): Industry name
            product_type (str): Type of product
            region (str, optional): Geographic region
            
        Returns:
            list: Applicable standards and requirements
        """
        # Get standards for the industry
        industry_standards = self.get_standards_by_industry(industry)
        
        # Filter by region if specified
        if region:
            industry_standards = {k: v for k, v in industry_standards.items() 
                                if v.get('region') == region or v.get('region') == 'International'}
        
        # Determine applicable standards based on product type
        applicable_standards = []
        
        for standard_id, standard in industry_standards.items():
            # Check if standard applies to the product type
            applies = False
            
            # Check subcategory
            if standard.get('subcategory') == 'all':
                applies = True
            elif product_type.lower() in standard.get('subcategory', '').lower():
                applies = True
            
            # Add applicable standard
            if applies:
                applicable_standards.append({
                    'id': standard.get('id'),
                    'name': standard.get('name'),
                    'description': standard.get('description'),
                    'key_requirements': standard.get('key_requirements', []),
                    'mandatory': standard.get('mandatory', False),
                    'region': standard.get('region')
                })
        
        return applicable_standards
    
    def get_design_guidelines(self, industry, product_type):
        """
        Get design guidelines based on industry standards.
        
        Args:
            industry (str): Industry name
            product_type (str): Type of product
            
        Returns:
            dict: Design guidelines
        """
        # Get applicable standards
        applicable_standards = self.get_compliance_requirements(industry, product_type)
        
        # Extract design guidelines from standards
        guidelines = {
            'safety': [],
            'performance': [],
            'sustainability': [],
            'accessibility': [],
            'general': []
        }
        
        for standard in applicable_standards:
            # Categorize requirements into guideline categories
            for req in standard.get('key_requirements', []):
                category = 'general'
                
                # Determine category based on requirement text
                req_lower = req.lower()
                if any(term in req_lower for term in ['safety', 'hazard', 'protection', 'fire', 'flammability']):
                    category = 'safety'
                elif any(term in req_lower for term in ['performance', 'durability', 'strength', 'stability']):
                    category = 'performance'
                elif any(term in req_lower for term in ['sustainability', 'recyclability', 'environmental']):
                    category = 'sustainability'
                elif any(term in req_lower for term in ['accessibility', 'usability', 'ergonomic']):
                    category = 'accessibility'
                
                # Add guideline with source
                guidelines[category].append({
                    'guideline': req,
                    'source': f"{standard.get('id')} - {standard.get('name')}"
                })
        
        return guidelines
    
    def add_standard(self, standard_id, standard_data):
        """
        Add a new standard to the database.
        
        Args:
            standard_id (str): Standard identifier
            standard_data (dict): Standard information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate standard data
            required_fields = ['id', 'name', 'industry', 'description', 'key_requirements']
            for field in required_fields:
                if field not in standard_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add standard to database
            self.standards[standard_id] = standard_data
            logger.info(f"Added standard: {standard_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding standard: {str(e)}")
            return False
    
    def update_standard(self, standard_id, standard_data):
        """
        Update an existing standard in the database.
        
        Args:
            standard_id (str): Standard identifier
            standard_data (dict): Updated standard information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if standard_id not in self.standards:
                logger.error(f"Standard not found: {standard_id}")
                return False
            
            # Update standard data
            self.standards[standard_id].update(standard_data)
            logger.info(f"Updated standard: {standard_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating standard: {str(e)}")
            return False
    
    def delete_standard(self, standard_id):
        """
        Delete a standard from the database.
        
        Args:
            standard_id (str): Standard identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if standard_id not in self.standards:
                logger.error(f"Standard not found: {standard_id}")
                return False
            
            # Delete standard
            del self.standards[standard_id]
            logger.info(f"Deleted standard: {standard_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting standard: {str(e)}")
            return False


if __name__ == "__main__":
    # Example usage
    standards = IndustryStandards()
    
    # Get standards by industry
    furniture_standards = standards.get_standards_by_industry('furniture')
    print(f"Found {len(furniture_standards)} furniture standards")
    
    # Get mandatory standards
    mandatory_standards = standards.get_mandatory_standards('electronics', 'United States')
    print(f"Found {len(mandatory_standards)} mandatory electronics standards in the US")
    
    # Get compliance requirements
    requirements = standards.get_compliance_requirements('furniture', 'chair', 'North America')
    print(f"Found {len(requirements)} compliance requirements for chairs in North America")
    
    # Get design guidelines
    guidelines = standards.get_design_guidelines('furniture', 'chair')
    print(f"Found {sum(len(v) for v in guidelines.values())} design guidelines for chairs")
