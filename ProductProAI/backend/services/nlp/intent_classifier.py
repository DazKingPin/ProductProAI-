import logging
import re
import json
from .text_processor import TextProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntentClassifier:
    """
    Class for classifying user intents from text commands.
    Identifies the primary intent and secondary intents in user commands.
    """
    
    def __init__(self):
        """
        Initialize the IntentClassifier.
        """
        logger.info("Initializing IntentClassifier")
        self.text_processor = TextProcessor()
        self._load_intent_patterns()
    
    def _load_intent_patterns(self):
        """
        Load intent patterns for classification.
        """
        # Define intent patterns
        self.intent_patterns = {
            'create': [
                r'create', r'make', r'design', r'build', r'generate', r'develop',
                r'new', r'start', r'begin', r'craft'
            ],
            'modify': [
                r'modify', r'change', r'update', r'edit', r'adjust', r'alter',
                r'transform', r'revise', r'refine', r'tweak'
            ],
            'color': [
                r'color', r'recolor', r'paint', r'tint', r'shade', r'hue',
                r'coloring', r'colorize'
            ],
            'material': [
                r'material', r'texture', r'fabric', r'surface', r'finish',
                r'composition', r'make of', r'made of', r'made from', r'using'
            ],
            'shape': [
                r'shape', r'form', r'structure', r'geometry', r'contour',
                r'outline', r'silhouette', r'profile'
            ],
            'size': [
                r'size', r'resize', r'scale', r'dimension', r'proportion',
                r'enlarge', r'reduce', r'bigger', r'smaller', r'larger', r'wider',
                r'taller', r'shorter', r'thinner', r'thicker'
            ],
            'add': [
                r'add', r'insert', r'include', r'incorporate', r'attach',
                r'append', r'affix', r'put in', r'place'
            ],
            'remove': [
                r'remove', r'delete', r'eliminate', r'take out', r'exclude',
                r'get rid of', r'discard', r'omit'
            ],
            'analyze': [
                r'analyze', r'examine', r'inspect', r'evaluate', r'assess',
                r'review', r'check', r'study', r'investigate'
            ],
            'compare': [
                r'compare', r'contrast', r'differentiate', r'distinguish',
                r'match', r'versus', r'against', r'side by side'
            ],
            'save': [
                r'save', r'store', r'keep', r'preserve', r'record', r'retain',
                r'archive', r'backup', r'export'
            ],
            'load': [
                r'load', r'open', r'import', r'retrieve', r'access', r'get',
                r'fetch', r'bring up', r'restore'
            ],
            'undo': [
                r'undo', r'revert', r'rollback', r'go back', r'previous',
                r'cancel', r'reverse'
            ],
            'redo': [
                r'redo', r'repeat', r'again', r'restore', r'reapply'
            ],
            'help': [
                r'help', r'assist', r'guide', r'support', r'aid', r'explain',
                r'instruction', r'tutorial', r'how to', r'what is'
            ],
            'show': [
                r'show', r'display', r'view', r'see', r'reveal', r'present',
                r'exhibit', r'demonstrate', r'visualize'
            ],
            'hide': [
                r'hide', r'conceal', r'mask', r'cover', r'obscure', r'invisible',
                r'remove from view'
            ],
            'rotate': [
                r'rotate', r'turn', r'spin', r'pivot', r'revolve', r'twist',
                r'orientation', r'angle', r'direction'
            ],
            'move': [
                r'move', r'shift', r'relocate', r'reposition', r'transfer',
                r'displace', r'drag', r'slide', r'position'
            ],
            'duplicate': [
                r'duplicate', r'copy', r'clone', r'replicate', r'reproduce',
                r'mirror', r'double'
            ],
            'combine': [
                r'combine', r'merge', r'join', r'unite', r'fuse', r'integrate',
                r'blend', r'mix', r'group'
            ],
            'separate': [
                r'separate', r'split', r'divide', r'disconnect', r'detach',
                r'break apart', r'ungroup', r'isolate'
            ],
            'export': [
                r'export', r'download', r'output', r'extract', r'send', r'share'
            ],
            'render': [
                r'render', r'visualize', r'preview', r'generate image', r'create image',
                r'show preview', r'display render'
            ],
            'optimize': [
                r'optimize', r'improve', r'enhance', r'refine', r'perfect',
                r'streamline', r'upgrade', r'better', r'boost'
            ],
            'simulate': [
                r'simulate', r'test', r'try', r'experiment', r'model', r'emulate',
                r'virtual test', r'prototype'
            ]
        }
        
        # Compile patterns for efficiency
        self.compiled_patterns = {}
        for intent, patterns in self.intent_patterns.items():
            self.compiled_patterns[intent] = [re.compile(r'\b' + pattern + r'\b', re.IGNORECASE) for pattern in patterns]
    
    def classify_intent(self, text):
        """
        Classify the primary and secondary intents in a text command.
        
        Args:
            text (str): Input text command
            
        Returns:
            dict: Intent classification results
        """
        try:
            logger.info(f"Classifying intent for: {text}")
            
            # Process the command text
            command_info = self.text_processor.process_command(text)
            
            # Initialize intent scores
            intent_scores = {intent: 0 for intent in self.intent_patterns.keys()}
            
            # Score each intent based on pattern matches
            for intent, patterns in self.compiled_patterns.items():
                for pattern in patterns:
                    matches = pattern.findall(text.lower())
                    intent_scores[intent] += len(matches)
            
            # Determine primary intent (highest score)
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])
            
            # If no clear intent is found, default to 'create'
            if primary_intent[1] == 0:
                primary_intent = ('create', 1)
            
            # Determine secondary intents (any with score > 0, excluding primary)
            secondary_intents = []
            for intent, score in intent_scores.items():
                if score > 0 and intent != primary_intent[0]:
                    secondary_intents.append((intent, score))
            
            # Sort secondary intents by score (descending)
            secondary_intents.sort(key=lambda x: x[1], reverse=True)
            
            # Create intent classification result
            intent_classification = {
                'primary_intent': primary_intent[0],
                'primary_score': primary_intent[1],
                'secondary_intents': [intent for intent, _ in secondary_intents],
                'command_info': command_info
            }
            
            logger.info(f"Intent classification: {intent_classification}")
            return intent_classification
            
        except Exception as e:
            logger.error(f"Error classifying intent: {str(e)}")
            return {
                'primary_intent': 'unknown',
                'primary_score': 0,
                'secondary_intents': [],
                'error': str(e)
            }
    
    def get_intent_description(self, intent):
        """
        Get a description of what an intent means.
        
        Args:
            intent (str): Intent name
            
        Returns:
            str: Intent description
        """
        intent_descriptions = {
            'create': "Create a new design or product from scratch",
            'modify': "Modify or change an existing design",
            'color': "Change or specify the color of a design",
            'material': "Change or specify the material of a design",
            'shape': "Change or specify the shape of a design",
            'size': "Change or specify the size or dimensions of a design",
            'add': "Add a new element or feature to a design",
            'remove': "Remove an element or feature from a design",
            'analyze': "Analyze or evaluate a design",
            'compare': "Compare two or more designs",
            'save': "Save the current design",
            'load': "Load a saved design",
            'undo': "Undo the last action",
            'redo': "Redo a previously undone action",
            'help': "Get help or information",
            'show': "Show or display something",
            'hide': "Hide something from view",
            'rotate': "Rotate or change the orientation of a design",
            'move': "Move or reposition elements in a design",
            'duplicate': "Create a copy of a design or element",
            'combine': "Combine multiple designs or elements",
            'separate': "Separate or split a design into parts",
            'export': "Export or download a design",
            'render': "Generate a visual representation of a design",
            'optimize': "Optimize or improve a design",
            'simulate': "Simulate or test a design"
        }
        
        return intent_descriptions.get(intent, "Unknown intent")


if __name__ == "__main__":
    # Example usage
    classifier = IntentClassifier()
    
    # Test with sample commands
    test_commands = [
        "Create a new chair design with wooden legs",
        "Change the color of the table to red",
        "Make the sofa bigger by 20%",
        "Add a circular pattern to the top surface",
        "Show me designs similar to this one",
        "Analyze this product for sustainability"
    ]
    
    for command in test_commands:
        result = classifier.classify_intent(command)
        print(f"\nCommand: {command}")
        print(f"Primary Intent: {result['primary_intent']} (Score: {result['primary_score']})")
        print(f"Secondary Intents: {result['secondary_intents']}")
        print(f"Intent Description: {classifier.get_intent_description(result['primary_intent'])}")
