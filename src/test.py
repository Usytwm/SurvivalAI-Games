
from ai.llm.inferencia_llm import LLMInterface
from environment.map import Map
constructor = LLMInterface
description = "It's a small stage."
answer = constructor.create_Map(description)
print(answer)