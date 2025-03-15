import logging
import re
import json
from .text_processor import TextProcessor
from .intent_classifier import IntentClassifier

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EntityExtractor:
    """
    Class for extracting entities from user commands.
    Identifies products, attributes, values, and other relevant entities.
    """
    
    def __init__(self):
        """
        Initialize the EntityExtractor.
        """
        logger.info("Initializing EntityExtractor")
        self.text_processor = TextProcessor()
        self._load_entity_patterns()
    
    def _load_entity_patterns(self):
        """
        Load entity patterns for extraction.
        """
        # Define product categories and examples
        self.product_categories = {
            'furniture': [
                'chair', 'table', 'desk', 'sofa', 'couch', 'bed', 'bookshelf', 
                'cabinet', 'dresser', 'stool', 'bench', 'ottoman', 'nightstand',
                'wardrobe', 'shelf', 'drawer', 'armchair', 'recliner', 'loveseat'
            ],
            'electronics': [
                'phone', 'smartphone', 'laptop', 'computer', 'tablet', 'monitor',
                'keyboard', 'mouse', 'speaker', 'headphone', 'earphone', 'camera',
                'tv', 'television', 'remote', 'charger', 'router', 'watch', 'clock'
            ],
            'kitchenware': [
                'plate', 'bowl', 'cup', 'mug', 'glass', 'fork', 'knife', 'spoon',
                'pot', 'pan', 'kettle', 'blender', 'mixer', 'toaster', 'oven',
                'microwave', 'refrigerator', 'fridge', 'dishwasher', 'utensil'
            ],
            'fashion': [
                'shirt', 'pants', 'jeans', 'dress', 'skirt', 'jacket', 'coat',
                'sweater', 'hoodie', 'hat', 'cap', 'shoe', 'boot', 'sneaker',
                'sock', 'glove', 'scarf', 'belt', 'bag', 'purse', 'wallet'
            ],
            'packaging': [
                'box', 'container', 'bottle', 'jar', 'can', 'package', 'wrapper',
                'bag', 'pouch', 'envelope', 'carton', 'tube', 'case', 'crate',
                'basket', 'tray', 'label', 'tag', 'lid', 'cap'
            ],
            'home_goods': [
                'lamp', 'light', 'rug', 'carpet', 'curtain', 'pillow', 'cushion',
                'blanket', 'towel', 'vase', 'frame', 'mirror', 'clock', 'candle',
                'decoration', 'ornament', 'hanger', 'hook', 'holder', 'stand'
            ]
        }
        
        # Flatten product list for easier searching
        self.all_products = []
        for category, products in self.product_categories.items():
            self.all_products.extend(products)
        
        # Define attribute types
        self.attribute_types = {
            'color': [
                'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'black',
                'white', 'gray', 'brown', 'pink', 'cyan', 'magenta', 'turquoise',
                'silver', 'gold', 'navy', 'maroon', 'olive', 'teal'
            ],
            'material': [
                'wood', 'metal', 'plastic', 'glass', 'leather', 'fabric', 'ceramic',
                'concrete', 'stone', 'rubber', 'silicone', 'paper', 'aluminum',
                'steel', 'copper', 'brass', 'marble', 'granite', 'cotton', 'polyester'
            ],
            'shape': [
                'circle', 'square', 'rectangle', 'triangle', 'oval', 'hexagon',
                'pentagon', 'octagon', 'sphere', 'cube', 'cylinder', 'cone',
                'pyramid', 'star', 'heart', 'crescent', 'spiral', 'curved', 'angular'
            ],
            'size': [
                'small', 'medium', 'large', 'tiny', 'huge', 'compact', 'wide',
                'narrow', 'tall', 'short', 'thick', 'thin', 'big', 'little'
            ],
            'style': [
                'modern', 'traditional', 'contemporary', 'classic', 'vintage',
                'rustic', 'industrial', 'minimalist', 'elegant', 'casual',
                'formal', 'bohemian', 'scandinavian', 'mid-century', 'art deco'
            ]
        }
        
        # Define measurement units
        self.measurement_units = {
            'length': ['mm', 'cm', 'meter', 'm', 'inch', 'in', 'ft', 'foot', 'feet', 'yard', 'yd'],
            'weight': ['g', 'gram', 'kg', 'kilogram', 'oz', 'ounce', 'lb', 'pound'],
            'volume': ['ml', 'milliliter', 'l', 'liter', 'oz', 'fluid ounce', 'cup', 'pint', 'quart', 'gallon'],
            'percentage': ['%', 'percent', 'percentage']
        }
        
        # Compile regex patterns for products
        self.product_patterns = {}
        for product in self.all_products:
            self.product_patterns[product] = re.compile(r'\b' + product + r'(?:s)?\b', re.IGNORECASE)
        
        # Compile regex patterns for attributes
        self.attribute_patterns = {}
        for attr_type, attributes in self.attribute_types.items():
            for attr in attributes:
                self.attribute_patterns[attr] = (attr_type, re.compile(r'\b' + attr + r'\b', re.IGNORECASE))
    
    def extract_entities(self, text):
        """
        Extract entities from text.
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Extracted entities
        """
        try:
            logger.info(f"Extracting entities from: {text}")
            
            # Initialize entities
            entities = {
                'products': [],
                'attributes': {
                    'color': [],
                    'material': [],
                    'shape': [],
                    'size': [],
                    'style': []
                },
                'measurements': [],
                'locations': [],
                'actions': []
            }
            
            # Extract products
            for product, pattern in self.product_patterns.items():
                if pattern.search(text):
                    category = next((cat for cat, prods in self.product_categories.items() if product in prods), 'other')
                    entities['products'].append({
                        'name': product,
                        'category': category
                    })
            
            # Extract attributes
            for attr, (attr_type, pattern) in self.attribute_patterns.items():
                if pattern.search(text):
                    entities['attributes'][attr_type].append(attr)
            
            # Extract measurements using text processor
            numeric_values = self.text_processor.extract_numeric_values(text)
            
            for value_type, value in numeric_values:
                # Check if there's a unit mentioned near the number
                for unit_type, units in self.measurement_units.items():
                    for unit in units:
                        unit_pattern = re.compile(r'\b' + str(value) + r'\s*' + unit + r'\b', re.IGNORECASE)
                        if unit_pattern.search(text):
                            entities['measurements'].append({
                                'value': value,
                                'unit': unit,
                                'type': unit_type
                            })
                            break
                    else:
                        continue
                    break
                else:
                    # No unit found, just add the numeric value
                    entities['measurements'].append({
                        'value': value,
                        'unit': None,
                        'type': value_type
                    })
            
            # Extract locations (e.g., "on the top", "at the bottom")
            location_patterns = {
                'top': r'\bon\s+(?:the\s+)?top\b|\btop\s+(?:of|part)\b',
                'bottom': r'\bon\s+(?:the\s+)?bottom\b|\bbottom\s+(?:of|part)\b',
                'left': r'\bon\s+(?:the\s+)?left\b|\bleft\s+(?:of|side)\b',
                'right': r'\bon\s+(?:the\s+)?right\b|\bright\s+(?:of|side)\b',
                'front': r'\bon\s+(?:the\s+)?front\b|\bfront\s+(?:of|part)\b',
                'back': r'\bon\s+(?:the\s+)?back\b|\bback\s+(?:of|part)\b',
                'center': r'\bin\s+(?:the\s+)?center\b|\bcenter\s+(?:of)?\b|\bmiddle\b',
                'inside': r'\binside\b|\bwithin\b|\binner\b',
                'outside': r'\boutside\b|\bouter\b|\bexterior\b'
            }
            
            for location, pattern in location_patterns.items():
                if re.search(pattern, text, re.IGNORECASE):
                    entities['locations'].append(location)
            
            # Extract actions (e.g., "rotate", "move", "scale")
            action_patterns = {
                'rotate': r'\brotate\b|\bturn\b|\bspin\b',
                'move': r'\bmove\b|\bshift\b|\breposition\b',
                'scale': r'\bscale\b|\bresize\b|\bmake\s+(?:bigger|smaller|larger)\b',
                'add': r'\badd\b|\binsert\b|\bplace\b',
                'remove': r'\bremove\b|\bdelete\b|\btake\s+(?:away|out)\b',
                'change': r'\bchange\b|\bmodify\b|\balter\b',
                'combine': r'\bcombine\b|\bmerge\b|\bjoin\b',
                'separate': r'\bseparate\b|\bsplit\b|\bdivide\b'
            }
            
            for action, pattern in action_patterns.items():
                if re.search(pattern, text, re.IGNORECASE):
                    entities['actions'].append(action)
            
            logger.info(f"Extracted entities: {entities}")
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {
                'products': [],
                'attributes': {
                    'color': [],
                    'material': [],
                    'shape': [],
                    'size': [],
                    'style': []
                },
                'measurements': [],
                'locations': [],
                'actions': [],
                'error': str(e)
            }
    
    def extract_relationships(self, text, entities):
        """
        Extract relationships between entities.
        
        Args:
            text (str): Input text
            entities (dict): Extracted entities
            
        Returns:
            dict: Entity relationships
        """
        relationships = {
            'product_attributes': [],
            'product_actions': [],
            'attribute_locations': []
        }
        
        # Extract product-attribute relationships
        for product in entities['products']:
            product_name = product['name']
            
            # Check if attributes are mentioned in relation to this product
            for attr_type, attrs in entities['attributes'].items():
                for attr in attrs:
                    # Check if the attribute is mentioned close to the product
                    # (within a window of words)
                    words = text.lower().split()
                    try:
                        product_indices = [i for i, word in enumerate(words) if product_name in word]
                        attr_indices = [i for i, word in enumerate(words) if attr in word]
                        
                        for p_idx in product_indices:
                            for a_idx in attr_indices:
                                # If they're within 5 words of each other, consider them related
                                if abs(p_idx - a_idx) <= 5:
                                    relationships['product_attributes'].append({
                                        'product': product_name,
                                        'attribute_type': attr_type,
                                        'attribute': attr
                                    })
                    except:
                        # If there's an error, just skip this relationship
                        pass
        
        # Extract product-action relationships
        for product in entities['products']:
            product_name = product['name']
            
            for action in entities['actions']:
                # Check if the action is mentioned close to the product
                words = text.lower().split()
                try:
                    product_indices = [i for i, word in enumerate(words) if product_name in word]
                    action_indices = [i for i, word in enumerate(words) if action in word]
                    
                    for p_idx in product_indices:
                        for a_idx in action_indices:
                            # If they're within 5 words of each other, consider them related
                            if abs(p_idx - a_idx) <= 5:
                                relationships['product_actions'].append({
                                    'product': product_name,
                                    'action': action
                                })
                except:
                    # If there's an error, just skip this relationship
                    pass
        
        # Extract attribute-location relationships
        for attr_type, attrs in entities['attributes'].items():
            for attr in attrs:
                for location in entities['locations']:
                    # Check if the attribute is mentioned close to the location
                    words = text.lower().split()
                    try:
                        attr_indices = [i for i, word in enumerate(words) if attr in word]
                        loc_pattern = '\\b' + location + '\\b'
                        loc_indices = [i for i, word in enumerate(words) if re.search(loc_pattern, word)]
                        
                        for a_idx in attr_indices:
                            for l_idx in loc_indices:
                                # If they're within 5 words of each other, consider them related
                                if abs(a_idx - l_idx) <= 5:
                                    relationships['attribute_locations'].append({
                                        'attribute_type': attr_type,
                                        'attribute': attr,
                                        'location': location
                                    })
                    except:
                        # If there's an error, just skip this relationship
                        pass
        
        return relationships


if __name__ == "__main__":
    # Example usage
    extractor = EntityExtractor()
    
    # Test with sample commands
    test_commands = [
        "Create a wooden chair with red cushions",
        "Make the table larger and add a glass top",
        "Design a modern sofa with leather upholstery",
        "Change the color of the lamp to blue",
        "Add metal legs to the bottom of the desk"
    ]
    
    for command in test_commands:
        entities = extractor.extract_entities(command)
        relationships = extractor.extract_relationships(command, entities)
        
        print(f"\nCommand: {command}")
        print(f"Products: {entities['products']}")
        print(f"Attributes: {entities['attributes']}")
        print(f"Actions: {entities['actions']}")
        print(f"Locations: {entities['locations']}")
        print(f"Relationships: {relationships}")
