import logging
import json
import random
from .command_parser import CommandParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResponseGenerator:
    """
    Class for generating appropriate responses to user commands.
    Converts parsed operations into natural language responses.
    """
    
    def __init__(self):
        """
        Initialize the ResponseGenerator.
        """
        logger.info("Initializing ResponseGenerator")
        self.command_parser = CommandParser()
        self._load_response_templates()
    
    def _load_response_templates(self):
        """
        Load response templates for different operation types.
        """
        # Define response templates for different operation types
        self.response_templates = {
            'create': [
                "I'll create {target_desc} {param_desc}.",
                "Creating {target_desc} {param_desc} as requested.",
                "I'm designing {target_desc} {param_desc} for you.",
                "Generating {target_desc} {param_desc} based on your specifications."
            ],
            'modify': [
                "I'll modify {target_desc} {param_desc}.",
                "Updating {target_desc} {param_desc} as requested.",
                "Making changes to {target_desc} {param_desc}.",
                "Adjusting {target_desc} {param_desc} according to your specifications."
            ],
            'color': [
                "I'll change the color of {target_desc} to {param_desc}.",
                "Updating the color of {target_desc} to {param_desc}.",
                "Applying {param_desc} color to {target_desc}.",
                "Recoloring {target_desc} with {param_desc}."
            ],
            'material': [
                "I'll change the material of {target_desc} to {param_desc}.",
                "Updating the material of {target_desc} to {param_desc}.",
                "Applying {param_desc} material to {target_desc}.",
                "Reconstructing {target_desc} with {param_desc}."
            ],
            'shape': [
                "I'll change the shape of {target_desc} to {param_desc}.",
                "Updating the shape of {target_desc} to {param_desc}.",
                "Reshaping {target_desc} to {param_desc}.",
                "Transforming {target_desc} into {param_desc} shape."
            ],
            'size': [
                "I'll change the size of {target_desc} to {param_desc}.",
                "Updating the dimensions of {target_desc} to {param_desc}.",
                "Resizing {target_desc} to {param_desc}.",
                "Adjusting the scale of {target_desc} to {param_desc}."
            ],
            'add': [
                "I'll add {param_desc} to {target_desc}.",
                "Adding {param_desc} to {target_desc} as requested.",
                "Incorporating {param_desc} into {target_desc}.",
                "Enhancing {target_desc} with {param_desc}."
            ],
            'remove': [
                "I'll remove {param_desc} from {target_desc}.",
                "Removing {param_desc} from {target_desc} as requested.",
                "Taking {param_desc} off {target_desc}.",
                "Eliminating {param_desc} from {target_desc}."
            ],
            'analyze': [
                "I'll analyze {target_desc} {param_desc}.",
                "Analyzing {target_desc} {param_desc} as requested.",
                "Examining {target_desc} {param_desc} in detail.",
                "Evaluating {target_desc} {param_desc} for you."
            ],
            'show': [
                "I'll show you {target_desc} {param_desc}.",
                "Displaying {target_desc} {param_desc} as requested.",
                "Here's {target_desc} {param_desc}.",
                "Presenting {target_desc} {param_desc} for your review."
            ],
            'rotate': [
                "I'll rotate {target_desc} {param_desc}.",
                "Rotating {target_desc} {param_desc} as requested.",
                "Turning {target_desc} {param_desc}.",
                "Adjusting the orientation of {target_desc} {param_desc}."
            ],
            'move': [
                "I'll move {target_desc} {param_desc}.",
                "Moving {target_desc} {param_desc} as requested.",
                "Repositioning {target_desc} {param_desc}.",
                "Shifting {target_desc} {param_desc}."
            ],
            'default': [
                "I'll process your request for {target_desc} {param_desc}.",
                "Working on your request for {target_desc} {param_desc}.",
                "Processing your instructions for {target_desc} {param_desc}.",
                "Executing your command for {target_desc} {param_desc}."
            ]
        }
        
        # Define follow-up questions for different operation types
        self.follow_up_questions = {
            'create': [
                "Would you like to specify any additional details for this design?",
                "Are there any specific materials you'd prefer for this design?",
                "Would you like to see some color options for this design?",
                "Should I optimize this design for any particular use case?"
            ],
            'modify': [
                "Is there anything else you'd like to change about this design?",
                "Would you like to see how this design looks from different angles?",
                "Should I suggest any complementary modifications?",
                "Would you like to compare this modified design with the original?"
            ],
            'color': [
                "Would you like to see some complementary color options?",
                "Should I apply this color to the entire design or just specific parts?",
                "Would you like to see how this color looks in different lighting conditions?",
                "Would you like to adjust the shade or intensity of this color?"
            ],
            'material': [
                "Would you like information about the properties of this material?",
                "Should I suggest alternative materials with similar properties?",
                "Would you like to see how this material affects the weight and durability?",
                "Would you like to see this material with different finishes?"
            ],
            'shape': [
                "Would you like to adjust any specific dimensions of this shape?",
                "Should I suggest variations of this shape that might work well?",
                "Would you like to see how this shape affects the functionality?",
                "Would you like to round or sharpen any edges of this shape?"
            ],
            'size': [
                "Would you like to maintain the current proportions while resizing?",
                "Should I adjust any specific dimensions independently?",
                "Would you like to see how this size compares to standard measurements?",
                "Would you like to optimize this size for any specific constraints?"
            ],
            'default': [
                "Is there anything else you'd like me to help you with?",
                "Would you like to see more options or alternatives?",
                "Is there any aspect of the design you'd like me to focus on?",
                "Would you like me to explain any part of this process in more detail?"
            ]
        }
        
        # Define design suggestions for different operation types
        self.design_suggestions = {
            'create': [
                "For this type of design, consider incorporating ergonomic principles for better user comfort.",
                "This design could benefit from sustainable materials like recycled plastics or responsibly sourced wood.",
                "Consider adding modular components to make this design more versatile and adaptable.",
                "A minimalist approach might enhance the aesthetic appeal while reducing production costs."
            ],
            'modify': [
                "This modification could be complemented by adjusting the overall proportions for better balance.",
                "Consider how this change affects the usability and accessibility of the design.",
                "This modification might benefit from contrasting elements to create visual interest.",
                "Think about how this change affects the manufacturing process and assembly."
            ],
            'color': [
                "This color choice could be enhanced with subtle gradients or texture variations.",
                "Consider using this as a primary color with complementary accent colors for visual interest.",
                "This color works well with natural materials like wood or stone for a balanced look.",
                "For a cohesive design, consider using variations of this color throughout different components."
            ],
            'material': [
                "This material choice offers good durability, but consider the maintenance requirements.",
                "For sustainability, this material can be paired with recycled or biodegradable components.",
                "The texture of this material creates interesting visual and tactile experiences.",
                "Consider how this material performs in different environmental conditions."
            ],
            'shape': [
                "This shape offers good structural integrity while maintaining visual appeal.",
                "Consider softening certain edges for improved safety and ergonomics.",
                "This geometric form could be repeated at different scales for a cohesive design language.",
                "The negative space created by this shape can be as important as the shape itself."
            ],
            'size': [
                "This size works well for the intended purpose, but consider adjusting for different user demographics.",
                "Maintaining golden ratio proportions could enhance the aesthetic appeal at this size.",
                "Consider how this size affects portability and storage requirements.",
                "This scale works well, but consider offering size variations to accommodate different needs."
            ],
            'default': [
                "Consider how this design fits into the broader ecosystem of related products.",
                "User testing could provide valuable insights for further refinement of this design.",
                "Think about the lifecycle of this product, from manufacturing to eventual recycling or disposal.",
                "The simplest solution is often the most elegant and effective."
            ]
        }
    
    def generate_response(self, operation):
        """
        Generate a natural language response to a parsed operation.
        
        Args:
            operation (dict): Parsed operation from CommandParser
            
        Returns:
            dict: Response with message, follow-up, and suggestions
        """
        try:
            logger.info(f"Generating response for operation: {operation['operation_type']}")
            
            # Get operation components
            operation_type = operation['operation_type']
            targets = operation['targets']
            parameters = operation['parameters']
            
            # Generate target description
            target_desc = self._generate_target_description(targets)
            
            # Generate parameter description
            param_desc = self._generate_parameter_description(operation_type, parameters)
            
            # Select response template
            templates = self.response_templates.get(operation_type, self.response_templates['default'])
            template = random.choice(templates)
            
            # Fill in template
            message = template.format(target_desc=target_desc, param_desc=param_desc)
            
            # Select follow-up question
            follow_up_options = self.follow_up_questions.get(operation_type, self.follow_up_questions['default'])
            follow_up = random.choice(follow_up_options)
            
            # Select design suggestion
            suggestion_options = self.design_suggestions.get(operation_type, self.design_suggestions['default'])
            suggestion = random.choice(suggestion_options)
            
            # Create response
            response = {
                'message': message,
                'follow_up': follow_up,
                'suggestion': suggestion,
                'operation': operation
            }
            
            logger.info(f"Generated response: {response['message']}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                'message': f"I'll process your request: '{operation['original_text']}'.",
                'follow_up': "Is there anything specific you'd like me to focus on?",
                'suggestion': "Consider providing more details for better results.",
                'operation': operation,
                'error': str(e)
            }
    
    def _generate_target_description(self, targets):
        """
        Generate a description of the operation targets.
        
        Args:
            targets (list): Operation targets
            
        Returns:
            str: Target description
        """
        if not targets:
            return "the design"
        
        target_names = []
        for target in targets:
            name = target.get('name', 'item')
            
            # Add attributes if available
            if 'attributes' in target and target['attributes']:
                attrs = []
                for attr in target['attributes']:
                    attrs.append(f"{attr['value']} {attr['type']}")
                
                if attrs:
                    name = f"{' '.join(attrs)} {name}"
            
            target_names.append(name)
        
        if len(target_names) == 1:
            return f"the {target_names[0]}"
        else:
            return f"the {', '.join(target_names[:-1])} and {target_names[-1]}"
    
    def _generate_parameter_description(self, operation_type, parameters):
        """
        Generate a description of the operation parameters.
        
        Args:
            operation_type (str): Type of operation
            parameters (dict): Operation parameters
            
        Returns:
            str: Parameter description
        """
        param_parts = []
        
        # Handle different parameter types based on operation type
        if operation_type in ['create', 'modify']:
            # Add color parameters
            if 'color' in parameters and parameters['color']:
                colors = parameters['color']
                if len(colors) == 1:
                    param_parts.append(f"in {colors[0]} color")
                else:
                    param_parts.append(f"with colors {', '.join(colors)}")
            
            # Add material parameters
            if 'material' in parameters and parameters['material']:
                materials = parameters['material']
                if len(materials) == 1:
                    param_parts.append(f"made of {materials[0]}")
                else:
                    param_parts.append(f"using materials {', '.join(materials)}")
            
            # Add shape parameters
            if 'shape' in parameters and parameters['shape']:
                shapes = parameters['shape']
                if len(shapes) == 1:
                    param_parts.append(f"with a {shapes[0]} shape")
                else:
                    param_parts.append(f"incorporating {', '.join(shapes)} shapes")
            
            # Add size parameters
            if 'size' in parameters and parameters['size']:
                sizes = parameters['size']
                if len(sizes) == 1:
                    param_parts.append(f"in {sizes[0]} size")
                else:
                    param_parts.append(f"with {', '.join(sizes)} dimensions")
            
            # Add measurement parameters
            if 'measurements' in parameters and parameters['measurements']:
                measurements = []
                for measure in parameters['measurements']:
                    if measure.get('unit'):
                        measurements.append(f"{measure['value']} {measure['unit']}")
                    else:
                        measurements.append(str(measure['value']))
                
                if measurements:
                    param_parts.append(f"with measurements {', '.join(measurements)}")
            
            # Add location parameters
            if 'locations' in parameters and parameters['locations']:
                locations = parameters['locations']
                if len(locations) == 1:
                    param_parts.append(f"at the {locations[0]}")
                else:
                    param_parts.append(f"at the {', '.join(locations)}")
        
        elif operation_type in ['color', 'material', 'shape', 'size']:
            # For specific attribute operations
            if operation_type in parameters and parameters[operation_type]:
                values = parameters[operation_type]
                if len(values) == 1:
                    param_parts.append(f"{values[0]}")
                else:
                    param_parts.append(f"{', '.join(values)}")
        
        elif operation_type in ['add', 'remove']:
            # For add/remove operations
            items = []
            
            for attr_type, attrs in parameters.items():
                if attr_type not in ['locations', 'actions', 'measurements']:
                    items.extend(attrs)
            
            if items:
                if len(items) == 1:
                    param_parts.append(f"{items[0]}")
                else:
                    param_parts.append(f"{', '.join(items[:-1])} and {items[-1]}")
            
            # Add location if present
            if 'locations' in parameters and parameters['locations']:
                locations = parameters['locations']
                if len(locations) == 1:
                    param_parts.append(f"at the {locations[0]}")
                else:
                    param_parts.append(f"at the {', '.join(locations)}")
        
        elif operation_type in ['rotate', 'move']:
            # For rotate/move operations
            if 'directions' in parameters and parameters['directions']:
                directions = parameters['directions']
                if len(directions) == 1:
                    param_parts.append(f"to the {directions[0]}")
                else:
                    param_parts.append(f"to the {', '.join(directions)}")
            
            if 'measurements' in parameters and parameters['measurements']:
                measurements = []
                for measure in parameters['measurements']:
                    if measure.get('unit'):
                        measurements.append(f"{measure['value']} {measure['unit']}")
                    else:
                        measurements.append(str(measure['value']))
                
                if measurements:
                    param_parts.append(f"by {', '.join(measurements)}")
        
        # Combine parameter parts
        if param_parts:
            return ' '.join(param_parts)
        else:
            return ""
    
    def process_and_respond(self, text):
        """
        Process a user command and generate a response.
        
        Args:
            text (str): User command text
            
        Returns:
            dict: Response with message, follow-up, and suggestions
        """
        try:
            # Parse the command
            operation = self.command_parser.parse_command(text)
            
            # Generate response
            response = self.generate_response(operation)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing and responding: {str(e)}")
            return {
                'message': f"I'll do my best to process your request: '{text}'.",
                'follow_up': "Could you provide more details or clarify your request?",
                'suggestion': "Try using specific terms for colors, materials, shapes, or sizes.",
                'error': str(e)
            }


if __name__ == "__main__":
    # Example usage
    generator = ResponseGenerator()
    
    # Test with sample commands
    test_commands = [
        "Create a wooden chair with red cushions",
        "Make the table larger and add a glass top",
        "Change the color of the lamp to blue",
        "Add metal legs to the bottom of the desk",
        "Rotate the sofa 90 degrees clockwise"
    ]
    
    for command in test_commands:
        response = generator.process_and_respond(command)
        
        print(f"\nCommand: {command}")
        print(f"Response: {response['message']}")
        print(f"Follow-up: {response['follow_up']}")
        print(f"Suggestion: {response['suggestion']}")
