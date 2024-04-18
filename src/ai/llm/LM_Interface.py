from openai import OpenAI
import re

class LLMInterface:
    def __init__(self) -> None:
        self.connect()
    def connect(self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio") -> bool:
        try:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            return True
        except:
            print("Error al acceder al modelo desde el programa xd")
            return False

    def create_Agent(self, character_resume: str):
        # Prepare the list of characteristics for the prompt
        system_content = f"""
        Prompt:

            Given a character description provided by the user, analyze and generate a 4-tuple of integers representing the character's life, consumption, movement, and vision. The characteristics are defined as follows:

            Life: A number from 1 to 15, with low values (1-5) indicating low life, medium values (6-10) indicating medium life, and high values (11-15) indicating high life.

            Consumption: A number from 1 to 9, with low values (1-3) indicating low consumption, medium values (4-6) indicating medium consumption, and high values (7-9) indicating high consumption.

            Movement: A number from 1 to 5, with low values (1-2) indicating low movement, medium values (3-4) indicating medium movement, and a high value (5) indicating high movement.

            Vision: A number from 1 to 5, with low values (1) indicating low vision, medium values (2-4) indicating medium vision, and high values (5) indicating high vision.

            You should interpret the user's description and adjust the values for each characteristic accordingly. If the user describes a positive aspect of the character, it should result in high values for the related characteristics. If the user describes a negative aspect, it should result in low values. If the user does not mention a particular aspect, you should assign medium values to that characteristic.

            User's character description:
            {character_resume}
            (e.g., character description: "bla bla"
                good direct output:
                * Life:  int
                * Consumption: int
                * Movement: int
                * Vision: int
            
            Direct Output:

                * Life:  (Integer representing the Life)
                * Consumption: (Integer representing the Consumption)
                * Movement: (Integer representing the Movement)
                * Vision: (Integer representing the Vision)
        """

        # Request for resumes to the model
        completation = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": character_resume},
            ],
            temperature=1.0,
        )

        # Get the response from the model
        response = completation.choices[0].message.content
        print(response)
        patron = r':\s*(\d+)'

        # Buscar coincidencias en el string
        answer = re.findall(patron, response)
        print(answer)
        return answer
    
    def create_Map(self, world_description: str):
        print(world_description)

        system_content = f"""
        Prompt:
    
        Given a description of a map, determine the appropriate width and height for the map based on its size description (small, medium, or large). 
    
        Here's a reference for size categories:
    
        | Size | Dimensions |
        |---|---|
        | Small | 10x10 units |
        | Medium | 25x25 units |
        | Large | 50x50 units |
    
        User's map description:
        {world_description}
        (e.g., "A small grassy plain" 
                direct output:
                    width: 10
                    heigth: 10
        )
        (e.g., "A small country" 
            good  direct output:
                    width: 50
                    heigth: 50
            good  direct output:
                    width: 10
                    heigth: 10
            bad   direct output:
                    " Given the description \"It's a small country,\" the appropriate width for the map is 50 units and the appropriate height is 50 units."
        )
        Direct Output:
    
            *width: (Integer representing the width of the map)
            *heigth: (Integer representing the height of the map)
        """
    
        completation = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": world_description},
            ],
            temperature=1.0,
        )
    
        response = completation.choices[0].message.content
        print(response)
        patron = r':\s*(\d+)'

        # Buscar coincidencias en el string
        answer = re.findall(patron, response)
    
        return answer