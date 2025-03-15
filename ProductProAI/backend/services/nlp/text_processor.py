import nltk
import logging
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextProcessor:
    """
    Class for processing and normalizing text input from users.
    Handles tokenization, lemmatization, and other text preprocessing tasks.
    """
    
    def __init__(self):
        """
        Initialize the TextProcessor.
        """
        logger.info("Initializing TextProcessor")
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.punctuation_translator = str.maketrans('', '', string.punctuation)
        
    def preprocess_text(self, text):
        """
        Preprocess text by converting to lowercase, removing punctuation,
        tokenizing, removing stop words, and lemmatizing.
        
        Args:
            text (str): Input text to preprocess
            
        Returns:
            list: List of preprocessed tokens
            str: Preprocessed text as a string
        """
        try:
            logger.info(f"Preprocessing text: {text}")
            
            # Convert to lowercase
            text = text.lower()
            
            # Remove punctuation
            text = text.translate(self.punctuation_translator)
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stop words and lemmatize
            filtered_tokens = []
            for token in tokens:
                if token not in self.stop_words:
                    lemmatized = self.lemmatizer.lemmatize(token)
                    filtered_tokens.append(lemmatized)
            
            # Join tokens back into a string
            preprocessed_text = ' '.join(filtered_tokens)
            
            logger.info(f"Preprocessed text: {preprocessed_text}")
            return filtered_tokens, preprocessed_text
            
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            return [], text
    
    def extract_keywords(self, text):
        """
        Extract keywords from text by removing stop words and keeping only
        nouns, verbs, adjectives, and adverbs.
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of keywords
        """
        try:
            # Tokenize and tag parts of speech
            tokens = word_tokenize(text.lower())
            tagged = nltk.pos_tag(tokens)
            
            # Keep only nouns, verbs, adjectives, and adverbs
            keywords = []
            for word, tag in tagged:
                if tag.startswith('N') or tag.startswith('V') or tag.startswith('J') or tag.startswith('R'):
                    if word not in self.stop_words and len(word) > 2:
                        keywords.append(word)
            
            logger.info(f"Extracted keywords: {keywords}")
            return keywords
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def normalize_color_terms(self, text):
        """
        Normalize color terms in text to standard color names.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized color terms
            list: List of detected colors
        """
        # Define color mappings
        color_mappings = {
            r'\bred\b': 'red',
            r'\bblue\b': 'blue',
            r'\bgreen\b': 'green',
            r'\byellow\b': 'yellow',
            r'\borange\b': 'orange',
            r'\bpurple\b': 'purple',
            r'\bblack\b': 'black',
            r'\bwhite\b': 'white',
            r'\bgray\b|\bgrey\b': 'gray',
            r'\bbrown\b': 'brown',
            r'\bpink\b': 'pink',
            r'\bcyan\b': 'cyan',
            r'\bmagenta\b': 'magenta',
            r'\bturquoise\b': 'turquoise',
            r'\bsilver\b': 'silver',
            r'\bgold\b': 'gold',
            r'\bnavy\b': 'navy blue',
            r'\bmaroon\b': 'maroon',
            r'\bolive\b': 'olive green',
            r'\bteal\b': 'teal'
        }
        
        detected_colors = []
        normalized_text = text.lower()
        
        for pattern, color in color_mappings.items():
            if re.search(pattern, normalized_text):
                detected_colors.append(color)
                normalized_text = re.sub(pattern, color, normalized_text)
        
        return normalized_text, detected_colors
    
    def normalize_material_terms(self, text):
        """
        Normalize material terms in text to standard material names.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized material terms
            list: List of detected materials
        """
        # Define material mappings
        material_mappings = {
            r'\bwood\b|\bwooden\b': 'wood',
            r'\bmetal\b|\bmetallic\b': 'metal',
            r'\bplastic\b': 'plastic',
            r'\bglass\b': 'glass',
            r'\bleather\b': 'leather',
            r'\bfabric\b|\bcloth\b|\btextile\b': 'fabric',
            r'\bceramic\b': 'ceramic',
            r'\bconcrete\b': 'concrete',
            r'\bstone\b': 'stone',
            r'\brubber\b': 'rubber',
            r'\bsilicone\b': 'silicone',
            r'\bpaper\b|\bcardboard\b': 'paper',
            r'\baluminum\b|\baluminium\b': 'aluminum',
            r'\bsteel\b': 'steel',
            r'\bcopper\b': 'copper',
            r'\bbrass\b': 'brass',
            r'\bmarble\b': 'marble',
            r'\bgranite\b': 'granite',
            r'\bcotton\b': 'cotton',
            r'\bpolyester\b': 'polyester',
            r'\bnylon\b': 'nylon',
            r'\bvelvet\b': 'velvet',
            r'\bsuede\b': 'suede',
            r'\bcork\b': 'cork',
            r'\bbamboo\b': 'bamboo'
        }
        
        detected_materials = []
        normalized_text = text.lower()
        
        for pattern, material in material_mappings.items():
            if re.search(pattern, normalized_text):
                detected_materials.append(material)
                normalized_text = re.sub(pattern, material, normalized_text)
        
        return normalized_text, detected_materials
    
    def normalize_shape_terms(self, text):
        """
        Normalize shape terms in text to standard shape names.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized shape terms
            list: List of detected shapes
        """
        # Define shape mappings
        shape_mappings = {
            r'\bcircle\b|\bcircular\b|\bround\b': 'circle',
            r'\bsquare\b': 'square',
            r'\brectangle\b|\brectangular\b': 'rectangle',
            r'\btriangle\b|\btriangular\b': 'triangle',
            r'\boval\b|\bellipse\b|\belliptical\b': 'oval',
            r'\bhexagon\b|\bhexagonal\b': 'hexagon',
            r'\bpentagon\b|\bpentagonal\b': 'pentagon',
            r'\boctagon\b|\boctagonal\b': 'octagon',
            r'\bsphere\b|\bspherical\b': 'sphere',
            r'\bcube\b|\bcubic\b': 'cube',
            r'\bcylinder\b|\bcylindrical\b': 'cylinder',
            r'\bcone\b|\bconical\b': 'cone',
            r'\bpyramid\b|\bpyramidal\b': 'pyramid',
            r'\bstar\b': 'star',
            r'\bheart\b': 'heart',
            r'\bcrescent\b': 'crescent',
            r'\bspiral\b': 'spiral',
            r'\bcurved\b|\bcurvy\b': 'curved',
            r'\bangular\b': 'angular',
            r'\bwavy\b': 'wavy',
            r'\bzig\s*zag\b': 'zigzag'
        }
        
        detected_shapes = []
        normalized_text = text.lower()
        
        for pattern, shape in shape_mappings.items():
            if re.search(pattern, normalized_text):
                detected_shapes.append(shape)
                normalized_text = re.sub(pattern, shape, normalized_text)
        
        return normalized_text, detected_shapes
    
    def normalize_size_terms(self, text):
        """
        Normalize size terms in text to standard size descriptors.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized size terms
            dict: Dictionary of detected size attributes
        """
        # Define size mappings
        size_increase_patterns = [
            r'\bbigger\b', r'\blarger\b', r'\bwider\b', r'\btaller\b', 
            r'\bincrease\b', r'\bexpand\b', r'\bgrow\b', r'\benlarge\b'
        ]
        
        size_decrease_patterns = [
            r'\bsmaller\b', r'\bnarrower\b', r'\bshorter\b', r'\bthinner\b',
            r'\bdecrease\b', r'\breduce\b', r'\bshrink\b', r'\bcontract\b'
        ]
        
        size_absolute_patterns = {
            r'\btiny\b|\bminuscule\b|\bvery\s+small\b': 'very_small',
            r'\bsmall\b|\bcompact\b': 'small',
            r'\bmedium\b|\bmoderate\b|\baverage\b': 'medium',
            r'\blarge\b|\bbig\b': 'large',
            r'\bhuge\b|\benormous\b|\bvery\s+large\b|\bvery\s+big\b': 'very_large'
        }
        
        # Check for size changes
        size_attributes = {}
        normalized_text = text.lower()
        
        # Check for increase patterns
        for pattern in size_increase_patterns:
            if re.search(pattern, normalized_text):
                size_attributes['change'] = 'increase'
                break
        
        # Check for decrease patterns
        for pattern in size_decrease_patterns:
            if re.search(pattern, normalized_text):
                size_attributes['change'] = 'decrease'
                break
        
        # Check for absolute size patterns
        for pattern, size in size_absolute_patterns.items():
            if re.search(pattern, normalized_text):
                size_attributes['absolute'] = size
                break
        
        # Check for specific dimensions
        width_patterns = [r'\bwidth\b', r'\bwide\b', r'\bwider\b']
        height_patterns = [r'\bheight\b', r'\btall\b', r'\btaller\b']
        depth_patterns = [r'\bdepth\b', r'\bdeep\b', r'\bdeeper\b']
        
        for pattern in width_patterns:
            if re.search(pattern, normalized_text):
                size_attributes['dimension'] = 'width'
                break
        
        for pattern in height_patterns:
            if re.search(pattern, normalized_text):
                size_attributes['dimension'] = 'height'
                break
        
        for pattern in depth_patterns:
            if re.search(pattern, normalized_text):
                size_attributes['dimension'] = 'depth'
                break
        
        return normalized_text, size_attributes
    
    def extract_numeric_values(self, text):
        """
        Extract numeric values from text.
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of numeric values
        """
        # Pattern for numbers (including decimals and percentages)
        number_pattern = r'\b\d+(?:\.\d+)?%?\b'
        
        # Find all matches
        matches = re.findall(number_pattern, text)
        
        # Convert to appropriate numeric types
        numeric_values = []
        for match in matches:
            if '%' in match:
                # Handle percentages
                value = float(match.replace('%', '')) / 100
                numeric_values.append(('percentage', value))
            elif '.' in match:
                # Handle decimals
                value = float(match)
                numeric_values.append(('decimal', value))
            else:
                # Handle integers
                value = int(match)
                numeric_values.append(('integer', value))
        
        return numeric_values
    
    def process_command(self, text):
        """
        Process a command by normalizing and extracting relevant information.
        
        Args:
            text (str): Input command text
            
        Returns:
            dict: Processed command information
        """
        try:
            logger.info(f"Processing command: {text}")
            
            # Initialize result
            command_info = {
                'original_text': text,
                'keywords': [],
                'colors': [],
                'materials': [],
                'shapes': [],
                'size': {},
                'numeric_values': []
            }
            
            # Preprocess text
            _, preprocessed_text = self.preprocess_text(text)
            command_info['preprocessed_text'] = preprocessed_text
            
            # Extract keywords
            command_info['keywords'] = self.extract_keywords(text)
            
            # Normalize and extract colors
            normalized_text, colors = self.normalize_color_terms(text)
            command_info['colors'] = colors
            
            # Normalize and extract materials
            normalized_text, materials = self.normalize_material_terms(normalized_text)
            command_info['materials'] = materials
            
            # Normalize and extract shapes
            normalized_text, shapes = self.normalize_shape_terms(normalized_text)
            command_info['shapes'] = shapes
            
            # Normalize and extract size information
            normalized_text, size_info = self.normalize_size_terms(normalized_text)
            command_info['size'] = size_info
            
            # Extract numeric values
            command_info['numeric_values'] = self.extract_numeric_values(text)
            
            logger.info(f"Command processed: {command_info}")
            return command_info
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return {
                'original_text': text,
                'error': str(e)
            }


if __name__ == "__main__":
    # Example usage
    processor = TextProcessor()
    
    # Test with sample commands
    test_commands = [
        "Make the chair red with wooden legs",
        "Increase the size of the table by 20%",
        "Change the material to metal and make it more angular",
        "Add a circular pattern to the top surface",
        "Make it look more modern with glass and steel"
    ]
    
    for command in test_commands:
        result = processor.process_command(command)
        print(f"\nCommand: {command}")
        print(f"Processed: {result}")
