from ai.llm.LM_Interface import LLMInterface
from environment.map import Map
constructor = LLMInterface()
descriptionTheMap = "It's a small country."
descriptionTheAgent = "He's strong "
answer = constructor.create_Agent(descriptionTheAgent)
print(answer)
answerMap =  constructor.create_Map(descriptionTheMap)
print(answerMap)