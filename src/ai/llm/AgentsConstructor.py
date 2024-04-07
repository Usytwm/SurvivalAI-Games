from inferencia_llm import LLMInterface

class AgentsBuild:

    def __init__(self, types_characters):
        self._llm_interface = LLMInterface()
        self._types_characters = types_characters

    def update_types(self, types_characters):
        self._types_characters = types_characters

    def create_agents(self, description: str):
        self._llm_interface.connect()
        
        return self._llm_interface.create_agent(description, self._types_characters)






    
        

    