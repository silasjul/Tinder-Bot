import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from pydantic import SecretStr
import os

# Configure browser
config = BrowserConfig(chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
browser = Browser(config=config)

# Configure LLM
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

# Create agent
agent = Agent(
    task="""
    Find a recipe of a great wedding cake.
""",
    llm=llm,
    initial_actions=[{'open_tab': {'url': 'https://www.google.com'}}],
    browser=browser
)

async def main():
    result = await agent.run()
    print(result)

    await browser.close()

    
if __name__ == '__main__':
    asyncio.run(main())