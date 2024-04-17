
from ai.llm.LM_Interface import LLMInterface
from environment.map import Map
constructor = LLMInterface()
constructor.connect()
descriptionTheMap = "It's a small country."
descriptionTheAgent = "He's strong "
answer = constructor.create_Map(descriptionTheMap)
print(answer)