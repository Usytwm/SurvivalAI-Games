from inferencia_llm import LLMInterface

class MapBuild:

    def __init__(self):
        self._llm_interface = LLMInterface()
        
    def create_Map(self, description: str):
        self._llm_interface.connect()
        
        return self._llm_interface.create_Map(description)


