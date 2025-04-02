from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Should be
msg_log = [
    "Me: Du ser godt ud 😍",
    "Her: Tak"
    "Me: Udover at se godt ud 😉, hvad bruger du så tiden på?"
    "Her: Ahahah går i skole"
    "Me: Fedt nok! Hvad læser du?"
    "Her: Går på katedralen. Så.."
    "Me: Okay, Katedralskolen cool nok! Men hvad laver du så, når du *ikke* drukner i lektier? 😉"
    "Her: Slapper af og hygger med venner oig familie. Hvad med dig?"
]

model = "gemini-2.5-pro-exp-03-25"
config = types.GenerateContentConfig(
    system_instruction="You are an expert dating coach that specialize in online dating conversations.",
)

prompt = f"""
        Here is the recent conversation history between a user (Me: a 23 yo software student at SDU. I love skiing, skydiving, hiking and indoor bouldering/climbing) 
        and a girl (Her: Pretty girl i like) on a dating app:
        {"\n".join(msg_log)}

        The user wants to {"ask her on a date" if len(msg_log) >= 4 else "know more about girl"}. Your task is to generate a short message in Danish that the user can send next.

        **IMPORTANT:** Generate *only* the Danish message text itself. 
        * Do NOT include any explanation or commentary.
        * Do NOT include any introductory phrases like "Here is a message you could send:".
        * Do NOT offer multiple options.
        * The output should be the raw message string ready to be copied and pasted.
        """

def getMessage():
    response = client.models.generate_content(model=model, config=config, contents=prompt)
    return response.text

message = getMessage()

print(message)