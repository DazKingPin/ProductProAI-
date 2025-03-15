import logging
import json
from .text_processor import TextProcessor
from .intent_classifier import IntentClassifier
from .entity_extractor import EntityExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CommandParser:
    """
    Class for parsing user commands into structured operations.
    Integrates text processing, intent classification, and entity extraction.
    """
    
    def __init__(self):
        """
        Initialize the CommandParser.
        """
        logger.info("Initializing CommandParser")
        self.text_processor = TextProcessor()
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
    
    def parse_command(self, text):
        """
        Parse a user command into a structured operation.
        
        Args:
            text (str): User command text
            
        Returns:
            dict: Structured command operation
        """
        try:
            logger.info(f"Parsing command: {text}")
            
            # Classify intent
            intent_classification = self.intent_classifier.classify_intent(text)
            
            # Extract entities
            entities = self.entity_extractor.extract_entities(text)
            
            # Extract relationships between entities
            relationships = self.entity_extractor.extract_relationships(text, entities)
            
            # Create structured operation
            operation = self._create_operation(text, intent_classification, entities, relationships)
            
            logger.info(f"Parsed operation: {operation}")
            return operation
            
        except Exception as e:
            logger.error(f"Error parsing command: {str(e)}")
            return {
                'original_text': text,
                'status': 'error',
                'error': str(e)
            }
    
    def _create_operation(self, text, intent_classification, entities, relationships):
        """
        Create a structured operation from parsed components.
        
        Args:
            text (str): Original command text
            intent_classification (dict): Intent classification results
            entities (dict): Extracted entities
            relationships (dict): Entity relationships
            
        Returns:
            dict: Structured operation
        """
        # Get primary and secondary intents
        primary_intent = intent_classification['primary_intent']
        secondary_intents = intent_classification['secondary_intents']
        
        # Create base operation
        operation = {
            'original_text': text,
            'status': 'success',
            'operation_type': primary_intent,
            'secondary_operations': secondary_intents,
            'targets': self._determine_targets(entities, relationships),
            'parameters': self._determine_parameters(primary_intent, entities, relationships),
            'context': {
                'entities': entities,
                'relationships': relationships
            }
        }
        
        return operation
    
    def _determine_targets(self, entities, relationships):
        """
        Determine the targets of the operation.
        
        Args:
            entities (dict): Extracted entities
            relationships (dict): Entity relationships
            
        Returns:
            list: Operation targets
        """
        targets = []
        
        # Add products as targets
        for product in entities['products']:
            target = {
                'type': 'product',
                'name': product['name'],
                'category': product['category']
            }
            
            # Add attributes related to this product
            target_attributes = []
            for rel in relationships['product_attributes']:
                if rel['product'] == product['name']:
                    target_attributes.append({
                        'type': rel['attribute_type'],
                        'value': rel['attribute']
                    })
            
            if target_attributes:
                target['attributes'] = target_attributes
            
            targets.append(target)
        
        # If no specific products were mentioned, add a generic target
        if not targets:
            targets.append({
                'type': 'generic',
                'name': 'current_design'
            })
        
        return targets
    
    def _determine_parameters(self, intent, entities, relationships):
        """
        Determine the parameters for the operation based on intent and entities.
        
        Args:
            intent (str): Primary intent
            entities (dict): Extracted entities
            relationships (dict): Entity relationships
            
        Returns:
            dict: Operation parameters
        """
        parameters = {}
        
        # Add parameters based on intent
        if intent in ['create', 'modify']:
            # Add attributes as parameters
            for attr_type, attrs in entities['attributes'].items():
                if attrs:
                    parameters[attr_type] = attrs
            
            # Add measurements as parameters
            if entities['measurements']:
                parameters['measurements'] = entities['measurements']
            
            # Add locations as parameters
            if entities['locations']:
                parameters['locations'] = entities['locations']
        
        elif intent in ['color', 'material', 'shape', 'size']:
            # For specific attribute intents, add those attributes as parameters
            if intent == 'color' and entities['attributes']['color']:
                parameters['color'] = entities['attributes']['color']
            elif intent == 'material' and entities['attributes']['material']:
                parameters['material'] = entities['attributes']['material']
            elif intent == 'shape' and entities['attributes']['shape']:
                parameters['shape'] = entities['attributes']['shape']
            elif intent == 'size':
                # For size, add both size attributes and measurements
                if entities['attributes']['size']:
                    parameters['size'] = entities['attributes']['size']
                if entities['measurements']:
                    parameters['measurements'] = entities['measurements']
        
        elif intent in ['add', 'remove']:
            # For add/remove, determine what's being added/removed
            for attr_type, attrs in entities['attributes'].items():
                if attrs:
                    parameters[attr_type] = attrs
            
            # Add locations for placement
            if entities['locations']:
                parameters['locations'] = entities['locations']
        
        elif intent in ['rotate', 'move']:
            # For rotate/move, add directions and measurements
            if entities['locations']:
                parameters['directions'] = entities['locations']
            if entities['measurements']:
                parameters['measurements'] = entities['measurements']
        
        # Add actions as parameters
        if entities['actions']:
            parameters['actions'] = entities['actions']
        
        return parameters
    
    def generate_command_explanation(self, operation):
        """
        Generate a human-readable explanation of a parsed command.
        
        Args:
            operation (dict): Structured operation
            
        Returns:
            str: Human-readable explanation
        """
        try:
            # Get operation components
            operation_type = operation['operation_type']
            targets = operation['targets']
            parameters = operation['parameters']
            
            # Start with the operation type
            explanation = f"I'll {operation_type} "
            
            # Add targets
            if targets:
                target_names = [target['name'] for target in targets]
                if len(target_names) == 1:
                    explanation += f"the {target_names[0]} "
                else:
                    explanation += f"the {', '.join(target_names[:-1])} and {target_names[-1]} "
            
            # Add parameters based on operation type
            if operation_type in ['create', 'modify']:
                param_descriptions = []
                
                # Add color parameters
                if 'color' in parameters:
                    colors = parameters['color']
                    if len(colors) == 1:
                        param_descriptions.append(f"in {colors[0]} color")
                    else:
                        param_descriptions.append(f"with colors {', '.join(colors)}")
                
                # Add material parameters
                if 'material' in parameters:
                    materials = parameters['material']
                    if len(materials) == 1:
                        param_descriptions.append(f"made of {materials[0]}")
                    else:
                        param_descriptions.append(f"using materials {', '.join(materials)}")
                
                # Add shape parameters
                if 'shape' in parameters:
                    shapes = parameters['shape']
                    if len(shapes) == 1:
                        param_descriptions.append(f"with a {shapes[0]} shape")
                    else:
                        param_descriptions.append(f"incorporating {', '.join(shapes)} shapes")
                
                # Add size parameters
                if 'size' in parameters:
                    sizes = parameters['size']
                    if len(sizes) == 1:
                        param_descriptions.append(f"in {sizes[0]} size")
                    else:
                        param_descriptions.append(f"with {', '.join(sizes)} dimensions")
                
                # Add measurement parameters
                if 'measurements' in parameters:
                    measurements = []
                    for measure in parameters['measurements']:
                        if measure['unit']:
                            measurements.append(f"{measure['value']} {measure['unit']}")
                        else:
                            measurements.append(str(measure['value']))
                    
                    if measurements:
                        param_descriptions.append(f"with measurements {', '.join(measurements)}")
                
                # Add location parameters
                if 'locations' in parameters:
                    locations = parameters['locations']
                    if len(locations) == 1:
                        param_descriptions.append(f"at the {locations[0]}")
                    else:
                        param_descriptions.append(f"at the {', '.join(locations)}")
                
                # Combine parameter descriptions
                if param_descriptions:
                    explanation += f"{' '.join(param_descriptions)}"
            
            elif operation_type in ['color', 'material', 'shape', 'size']:
                # For specific attribute operations
                if operation_type in parameters and parameters[operation_type]:
                    values = parameters[operation_type]
                    if len(values) == 1:
                        explanation += f"to {values[0]}"
                    else:
                        explanation += f"to include {', '.join(values)}"
            
            elif operation_type in ['add', 'remove']:
                # For add/remove operations
                items_to_add = []
                
                for attr_type, attrs in parameters.items():
                    if attr_type not in ['locations', 'actions', 'measurements']:
                        items_to_add.extend(attrs)
                
                if items_to_add:
                    if len(items_to_add) == 1:
                        explanation += f"{items_to_add[0]}"
                    else:
                        explanation += f"{', '.join(items_to_add[:-1])} and {items_to_add[-1]}"
                
                # Add location if present
                if 'locations' in parameters:
                    locations = parameters['locations']
                    if len(locations) == 1:
                        explanation += f" at the {locations[0]}"
                    else:
                        explanation += f" at the {', '.join(locations)}"
            
            # Add a period at the end
            if not explanation.endswith('.'):
                explanation += '.'
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating command explanation: {str(e)}")
            return f"I'll process your request: '{operation['original_text']}'."


if __name__ == "__main__":
    # Example usage
    parser = CommandParser()
    
    # Test with sample commands
    test_commands = [
        "Create a wooden chair with red cushions",
        "Make the table larger and add a glass top",
        "Change the color of the lamp to blue",
        "Add metal legs to the bottom of the desk",
        "Rotate the sofa 90 degrees clockwise"
    ]
    
    for command in test_commands:
        operation = parser.parse_command(command)
        explanation = parser.generate_command_explanation(operation)
        
        print(f"\nCommand: {command}")
        print(f"Operation Type: {operation['operation_type']}")
        print(f"Targets: {operation['targets']}")
        print(f"Parameters: {operation['parameters']}")
        print(f"Explanation: {explanation}")
