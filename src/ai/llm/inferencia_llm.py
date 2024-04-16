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

    def create_agent(self, character_resume: str):
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
            Output:

                Life: [Generated value]
                Consumption: [Generated value]
                Movement: [Generated value]
                Vision: [Generated value]
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
        #response_parts = response.split("\n")
        #matching_feature_index = int(response_parts[2].split(":")[0]) - 1 # Adjust based on the actual response format
        #matching_feature = types_characters[matching_feature_index]
        #gender_and_name = response_parts[3].split(":")[1].strip()

        return response
    

    def create_Map(self, world_description: str):
        system_content = f"""
        Prompt:

            Given the user's description of a map, extract the width and height values that should be used to create the map.Taking a map of 10x10 as small, 200x200 as medium, and 500x500 as large. The description may include various details about the map, such as its size, terrain, and any objects or agents present.

            User's map description:
            {world_description}

        Output:

            The width and height values extracted from the user's description are: {width} x {height}
        """
        """
        # Format the system content with the actual world description
        formatted_system_content = system_content.format(world_description=world_description)
        """
        # Request for map dimensions to the model
        completation = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_content},
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