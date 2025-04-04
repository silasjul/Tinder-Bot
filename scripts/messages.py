from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

class MessageGenerator():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        self.model = "gemini-2.5-pro-exp-03-25"
        self.config = types.GenerateContentConfig(
            system_instruction="You are an expert dating coach that specialize in conversations.",
        )

    def generate(self, msg_log):

        goal = "ask her on a date (good date ideas: go indoor bouldering, go for a walk in 'munke mose', invite over for dinner. bad date ideas: drink coffee)" if len(msg_log) >= 4 else "know more about her"

        prompt = f"""
            Here is the recent conversation history between a user (Me: a 23 yo software student at SDU. Im physically active and my hobbies are playing guitar, hiking and indoor bouldering/climbing) 
            and a girl (Her: Pretty girl i like):
            {"\n".join(str(msg_log))}

            The user wants to {goal}. Your task is to generate a short text-message in Danish that the user can send.

            **IMPORTANT:** Generate *only* the Danish message text itself. 
            * Do NOT include any explanation or commentary.
            * Do NOT include any introductory phrases like "Here is a message you could send:".
            * Do NOT offer multiple options.
            * The output should be the raw message string ready to be copied and pasted.
        """
        response = self.client.models.generate_content(model=self.model, config=self.config, contents=prompt)
        return response.text
    
    def analyse_message(self, message):
        prompt = f"""
            Here is a text-message i recieved from a girl in Danish:
            {message}

            Your task is to analyse the message and generate a boolean for weather or not she agreed to go on a date with me.

            **IMPORTANT:** Generate *only* the Danish summary itself. 
            * Do NOT include any explanation or commentary.
            * Do NOT include any introductory phrases like "Here is a summary:".
            * The output should be a boolean like True or False.
        """
        response = self.client.models.generate_content(model=self.model, config=self.config, contents=prompt)
        return response.text == "True"


if __name__ == "__main__":
    example_log = [
            "Me: Du ser godt ud 😍",
            "Her: awww",
            "Her: tak i lige måde",
        ]
    message = MessageGenerator()

    print(message.analyse_message(example_log[-1]))