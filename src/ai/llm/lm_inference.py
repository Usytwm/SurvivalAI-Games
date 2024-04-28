from openai import OpenAI
import re

class LLMInterface:
    """
    Class to interact with a language model through the LMstudio API.
    Allows connecting to the model, creating agents based on descriptions, and generating maps.
    """
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
        """
        Creates an agent based on a description provided by the user.
        Analyzes the description and generates a 4-tuple of integers representing the character's life, consumption, movement, and vision.
        
        Parameters:
        - character_resume: Character description provided by the user.
        
        Returns:
        - A list of integers representing the character's life, consumption, movement, and vision.
        """
        # Prepare the list of characteristics for the prompt
        system_content = f"""
        Prompt:

            Given a character description provided by the user, analyze and generate a 4-tuple of integers representing the character's life, consumption, movement, and vision. The characteristics are defined as follows:

            Life: A number from 1 to 5, with low values (1) indicating low life, medium values (2) indicating medium life, and high values (3) indicating high life.

            Consumption: A number from 1 to 3, with low values (1) indicating low consumption, medium values (2) indicating medium consumption, and high values (3) indicating high consumption.

            Power: A number from 1 to 5, with low values (1-2) indicating low power, medium values (3-4) indicating medium power, and a high value (5) indicating high power

            Vision: A number from 1 to 4, with low values (1) indicating low vision, medium values (2-3) indicating medium vision, and high values (4) indicating high vision.

            You should interpret the user's description and adjust the values for each characteristic accordingly. If the user describes a positive aspect of the character, it should result in high values for the related characteristics. If the user describes a negative aspect, it should result in low values. If the user does not mention a particular aspect, you should assign medium values to that characteristic.

            User's character description:
            {character_resume}
            (e.g., character description: "bla bla"
                good direct output:
                * Life:  int
                * Consumption: int
                * Power: int
                * Vision: int
            
            Direct Output:

                * Life:  (Integer representing the Life)
                * Consumption: (Integer representing the Consumption)
                * Power: (Integer representing the Movement)
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
        #print(response)
        patron = r':\s*(\d+)'
        answer = re.findall(patron, response)
        #print(answer)
        return answer
    
    def create_Map(self, world_description: str):
        """
        Generates a map based on a description provided by the user.
        Determines the appropriate width and height for the map based on its size description (small, medium, or large).
        
        Parameters:
        - world_description: Map description provided by the user.
        
        Returns:
        - A list of integers representing the width and height of the map.
        """
        print(world_description)

        system_content = f"""
        Prompt:
    
        Given a description of a map, determine the appropriate width and height for the map based on its size description (small, medium, or large). 
    
        Here's a reference for size categories:
        
        | Size | Dimensions |
        |---|---|
        | Small | 10x10 units |
        | Medium | 20x20 units |
        | Large | 30x30 units |
    
        User's map description:
        {world_description}
        (e.g., "A small grassy plain" 
                direct output:
                    width: 10
                    heigth: 10
        )
        (e.g., "A small country" 
            good  direct output:
                    width: 30
                    heigth: 30
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
        #print(response)
        patron = r':\s*(\d+)'
        answer = re.findall(patron, response)
        return answer
    
    def create_History(self, character_list: str, messages):
        """
            Generates a narrative continuation for a survival game based on a given character list and action log.

            Parameters:
                character_list (str): A string containing a formatted list of characters with their IDs, first names, and descriptions.
                messages (str): A string representing the latest actions of the characters.

            Returns:
                str: A narrative continuation crafted by a narrator, aligning with the previous story and actions taken by the characters.
        """
        prompt = f"""
                You're a narrator for a survival game, employing a bold and dark tone in your commentary. Your greatest skill lies in taking a summary of a story and a log representing actions in the game, then crafting a new narrative that continues the previous one. Your aim is to create a coherent and meaningful story that aligns with what has happened before. You have the ability to develop the plot based on the action log and infuse personality into both successes and failures. Let your creativity soar!

                In the game, characters report their actions with their numerical ID, which consists of an integer. Below is a list of characters. Each item in the list contains the character's ID, their first name, and a brief description of them.
                Character List:
                {character_list}

        """
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                   
                },
                    {"role": "user", "content": "The latest actions of the characters"
                                                +"\n"
                                                + messages
                     },
            ],
            temperature=1.0,
        )
        # Get the response from the model
        response = completion.choices[0].message.content

        return response



    



    