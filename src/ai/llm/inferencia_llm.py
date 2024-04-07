from openai import OpenAI


class LLMInterface:
    MAIN_PROMPT = "create_character"

    def __init__(self):
        self._poblate_prompts()

    def connect(self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio") -> bool:
        try:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            return True
        except:
            print("Error al acceder al modelo desde el programa xd")
            return False

    def create_agent(self, character_resume: str, types_characters: list):
        # Prepare the list of characteristics for the prompt
        characteristics_prompt = "\n".join([f"{i+1} : {character}" for i, character in enumerate(types_characters)])
        
        system_content = f"""
        Prompt:

            From the provided list of characteristics, identify the feature that most closely resembles the user's character description. Additionally, determine the gender and name of the character as described by the user. If the gender or name is omitted, assign them randomly.

            Characteristics:
            {characteristics_prompt}

        Output:

            The character described by the user is: {character_resume}
            The feature that most closely resembles the user's character description is: {characteristics_prompt}
            The gender and name of the character are: {character_resume}
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

        # Extract the matching feature, gender, and name from the response
        response_parts = response.split("\n")
        matching_feature_index = int(response_parts[2].split(":")[0]) - 1 # Adjust based on the actual response format
        matching_feature = types_characters[matching_feature_index]
        gender_and_name = response_parts[3].split(":")[1].strip()

        return matching_feature, gender_and_name
    

    def create_Map(self, world_description: str):
        system_content = """
        Prompt:

            Given the user's description of a map, extract the width and height values that should be used to create the map.Taking a map of 10x10 as small, 200x200 as medium, and 500x500 as large. The description may include various details about the map, such as its size, terrain, and any objects or agents present.

            User's map description:
            {world_description}

        Output:

            The width and height values extracted from the user's description are: {width} x {height}
        """

        # Format the system content with the actual world description
        formatted_system_content = system_content.format(world_description=world_description)

        # Request for map dimensions to the model
        completation = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": formatted_system_content},
            ],
            temperature=1.0,
        )

        # Get the response from the model
        response = completation.choices[0].message.content

        # Extract the width and height from the response
        width, height = map(int, response.split("x"))

        return width, height
    

    def _poblate_prompts(self):
        """The prompts dictionary with the prompts for each task."""

        # Todo: Add more prompts 
        self.prompts = {
            self.MAIN_PROMPT: "You are bla bla.",
        }



    



    