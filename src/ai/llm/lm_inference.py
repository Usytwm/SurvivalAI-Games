import google.generativeai as genai
import os
import re

class LLMInterface:
    """
    Class to interact with a language model through the LMstudio API.
    Allows connecting to the model, creating agents based on descriptions, and generating maps.
    """
    def __init__(self) -> None:
        self.connect()
    
    def connect(self) -> bool:
        try:
            """Inicializa la clase y configura la API"""
            os.environ['API_KEY'] = "" #! Reemplaza con tu clave de API
            genai.configure(api_key=os.environ['API_KEY'])
            self.model = genai.GenerativeModel('gemini-pro')
        except:
            print("Error al acceder al modelo desde el programa xd")
            return False
        

    def create_Agents(self, character_resume: str, characters, default: int):
        respuesta = {}
        # Expresión regular para encontrar los comentarios
        patron_comentario = r'/\*(.*?)\*/'

        # Buscar todas las coincidencias de comentarios en el texto
        coincidencias = re.findall(patron_comentario, character_resume, re.DOTALL)

        # Imprimir los cuerpos de los comentarios encontrados
        for comentario in coincidencias:

            prompt_comparation = f"""
            Prompt:

            Given a list of character types and their descriptions, find the character type that best matches the user's description.

            User's Description:
            "{comentario.strip()}"

            Character Types and Descriptions:
            {characters}

            You should analyze the user's description and compare it with the descriptions of the character types to find the best match. If the user's description shares similarities with multiple character types, in {characters}. If in the description provided by the user it's not clear what type of character it is, it defaults to the character being of the "Random" type.
            Identify the number of characters of the returned type that appear in the description. If the provided user description does not allow obtaining the number of characters due to the context, return {default}.
            
            Direct Output:
                    *Type: [Type of Character]
                    *Cant: [Cant]
            (e.g: "He is bla bla")
                good Direct Output: 
                    *Type: string
                    *Cant: int
                bad Direct Output:
                    {{
                    "Type": string,
                    "Cant": int
                    }}

            """
            response_type = self.model.generate_content(
            prompt_comparation
            )

            #print(response_type.text)
            answer_type = re.search(r':\s+(.+)', response_type.text)
            answer_cant = re.search(r':\s*(\d+)', response_type.text)
            respuesta[answer_type.group(1)] = int(answer_cant.group(1))
    
        return respuesta
            
            
    def create_Agent(self, character_resume: str, characters):
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

            You should interpret the user's description and adjust the values for each characteristic accordingly. If the user describes a positive aspect of the character, it should result in high values for the related characteristics. If the user describes a negative aspect, it should result in low values. 
            If the user does not mention a particular phsic aspect, you should assign medium values to that characteristic.
            If you are unable to interpret the character description in terms of the provided characteristics, it defaults to returning the terms in medium ranges.
            Limit yourself to responding in the manner as shown in the examples; do not provide code.

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
        
        prompt_comparation = f"""
            Prompt:

            Given a list of character types and their descriptions, find the character type that best matches the user's description.

            User's Description:
            "{character_resume}"

            Character Types and Descriptions:
            {characters}

            You should analyze the user's description and compare it with the descriptions of the character types to find the best match. If the user's description shares similarities with multiple character types, in {characters}. If in the description provided by the user it's not clear what type of character it is, it defaults to the character being of the "Random" type.

            Direct Output:
            - Character Type: [Type of Character]
            (e.g: "He is bla bla")
                good Direct Output: 
                    *Type: string
        """
        
        # Request for resumes to the model
        response_values = self.model.generate_content(
            system_content
        )
        response_type = self.model.generate_content(
            prompt_comparation
        )
        print(response_type.text)
        
        # Get the response_values from the model
        
        print(response_values.text)
        patron = r':\s*(\d+)'
        answer = re.findall(patron, response_values.text)
        answer = [int(value) for value in answer]
        
        answer_type = re.search(r'- Character Type:\s+(.+)', response_type.text)

        return answer, answer_type.group(1)
    
    def create_Map(self, world_description: str, world_dimensions: tuple[int, int , int]):
        """
        Generates a map based on a description provided by the user.
        Determines the appropriate width and height for the map based on its size description (small, medium, or large).
        
        Parameters:
        - world_description: Map description provided by the user.
        - world_dimensions: The first, second, and third elements of the tuple represent the values small, medium, large respectively.
        
        Returns:
        - A list of integers representing the width and height of the map.
        """
        small, medium, big = world_dimensions
        system_content = f"""
        Prompt:
    
        Given a description of a map, determine the appropriate width and height for the map based on its size description (small, medium, or large). 
        If the user's description describes a terrain whose dimensions are different from each other, reflect it in the result.
        "If the user omits key information to identify the dimensions of the terrain or the information is not understood from the context, it defaults to returning the attributes in median dimensions."
        Here's a reference for size categories:
        
        | Size | Dimensions |
        |---|---|
        | Small | {small}x{small} units |
        | Medium | {medium}x{medium} units |
        | Large | {big}x{big} units |
    
        User's map description:
        {world_description}
        (e.g., "A small grassy plain" 
                direct output:
                    width: {small}
                    heigth: {small}
        )
        (e.g., "A country" 
            good  direct output:
                    width: {big}
                    heigth: {big}
            bad   direct output:
                    " Given the description \"It's a small country,\" the appropriate width for the map is 50 units and the appropriate height is 50 units."
        )
        Direct Output:
    
            *width: (Integer representing the width of the map)
            *heigth: (Integer representing the height of the map)
        """
    
        response_values = self.model.generate_content(
            system_content
        )
        print(response_values.text)
        patron = r':\s*(\d+)'
        answer = re.findall(patron, response_values.text)
        answer = [int(value) for value in answer]
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
                "The latest actions of the characters"
                +"\n"
                + {messages}

        """
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
            # Only one candidate for now.
            candidate_count=1,
            stop_sequences=['x'],
            max_output_tokens=300,
            temperature=1.0)
        )
        # Get the response_values from the model
        return response.text



    



    