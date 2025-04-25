import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import google
import json
load_dotenv()
with open("config.json", "r") as config_file:
    config = json.load(config_file)

class MessageGenerator():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = "gemini-2.5-pro-exp-03-25"
        self.config = types.GenerateContentConfig(
            system_instruction="You are an expert dating coach that specialize in texting and online dating.",
        )

    def generate_response(self, msg_log):
        prompt = f"""
            Here is the recent conversation history between 
            Me: {config["about_me"]}
            and
            Her: Pretty girl i like:
            {"\n".join(msg_log)}

            Your task is to generate a short text-message in Danish that I can send.

            **IMPORTANT:** Generate *only* the Danish message text itself. 
            * Do NOT include any explanation or commentary.
            * Do NOT include characters like *, / or @ in the message.
            * Do NOT include any introductory phrases like "Here is a message you could send:".
            * Do NOT ask her on a date too early
            * Do NOT offer multiple options.
            * The output should be the raw message string ready to be copied and pasted.
        """
        response = self.generate_content(prompt)
        return response.text
    
    def generate_date(self, msg_log):
        prompt = f"""
            Here is a conversation between:
            Me: a 23 yo software student at SDU. Im physically active and my hobbies are playing guitar, hiking and indoor climbing
            Her: Pretty girl i like
            {"\n".join(msg_log)}

            She accepted to go on a date with me, and i need you to generate a short text-message in Danish with date details i can send her.
            My date preference are: {config["date_preference"]}.

            **IMPORTANT:** Generate *only* the Danish message text itself. 
            * Do NOT include any explanation or commentary.
            * Do NOT include characters like *, / or @ in the message.
            * Do NOT include any introductory phrases like "Here is a message you could send:".
            * Do NOT offer multiple options.
            * The output should be the raw message string ready to be copied and pasted.
        """
        response = self.generate_content(prompt)
        return response.text

    def generate_opener(self, bio):
        if not bio or len(bio) <= 5:
            return 'Hvis jeg var en T-rex, ville jeg prøve at kramme dig med mine små arme også ligge mig ned og græde fordi jeg ikke kunne modstå din lækre menneskeduft og spise dig'

        prompt = f"""
            Her: Pretty girl I like on tinder. Her bio: {bio}):

            Your task is to generate a flirty conversation starting text-message in Danish that I can send.

            **IMPORTANT:** Generate *only* the Danish message text itself. 
            * Do NOT include any explanation or commentary.
            * Do NOT include characters like *, / or @ in the message.
            * Do NOT include any introductory phrases like "Here is a message you could send:".
            * Do NOT use english words or phrases in the message.
            * Do NOT ask her on a date
            * Do NOT offer multiple options.
            * The output should be the raw message string ready to be copied and pasted.
        """
        response = self.generate_content(prompt)
        return response.text
    
    def analyse_msg_log(self, msg_log):
        prompt = f"""
            Here are some text-messages between me and a girl in Danish:
            {"\n".join(msg_log)}

            Your task is to analyse the messages and generate a boolean for weather or not she agreed to go on a date with me.

            **IMPORTANT:** Generate *only* the Danish summary itself. 
            * Make sure i directly asked her out.
            * Do NOT include any explanation or commentary.
            * Do NOT include any introductory phrases like "Here is a summary:".
            * The output should be a boolean like True or False.
        """
        response = self.generate_content(prompt)
        return response.text == "True"
    
    
    def generate_content(self, prompt):
        try:
            return self.client.models.generate_content(model=self.model, config=self.config, contents=prompt)
        except google.genai.errors.ServerError:
            time.sleep(5)
            self.generate_content(prompt)



if __name__ == "__main__":
    example_log = [
            "Me: Så hvis jeg dukker op med en iskold Pepsi Max, er vejen til dit hjerte åben? 😉",
            "Her: Især hvis den er iskold ja",
        ]
    bio_example = 'Jeg laver fantastisk morgenmad og aftensmad, hvis du kan lide havregryn, og over-/underkogt pasta med ketchup👩‍🍳'

    message = MessageGenerator()
    print(message.generate_opener(bio_example))