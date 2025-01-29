import anthropic
from LLM_utils import make_system_prompt, make_user_prompt
import constants

class LLMClient:
    def __init__(self, code_input):
        self.client = anthropic.Anthropic(api_key = constants.CLAUDE_API_KEY)
        self.code_input = code_input

        # List to hold user queries and Claude's responses for maintaining contextual awareness
        self.messages = []

        # Making a system prompt to set Claude's role and feed the code.
        make_system_prompt(self.client, constants.SYSTEM_PROMPT+self.code_input, self.messages, constants.INITIAL_USER_QUERY)


    def get_response_to_query(self, query):
        """
        Prompts Claude and generates a response.
        """
        response_text = make_user_prompt(self.client, constants.SYSTEM_PROMPT+self.code_input, self.messages, query)
        return response_text