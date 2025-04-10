<div align="center">
<pre>
,---------. .-./`) ,---.   .--. ______         .-''-.  .-------.             _______       ,-----.  ,---------.
\          \\ .-.')|    \  |  ||    _ `''.   .'_ _   \ |  _ _   \           \  ____  \   .'  .-,  '.\          \
 `--.  ,---'/ `-' \|  ,  \ |  || _ | ) _  \ / ( ` )   '| ( ' )  |           | |    \ |  / ,-.|  \ _ \`--.  ,---'
    |   \    `-'`"`|  |\_ \|  ||( ''_'  ) |. (_ o _)  ||(_ o _) /           | |____/ / ;  \  '_ /  | :  |   \
    :_ _:    .---. |  _( )_\  || . (_) `. ||  (_,_)___|| (_,_).' __         |   _ _ '. |  _`,/ \ _/  |  :_ _:
    (_I_)    |   | | (_ o _)  ||(_    ._) ''  \   .---.|  |\ \  |  |        |  ( ' )  \: (  '\_/ \   ;  (_I_)
   (_(=)_)   |   | |  (_,_)\  ||  (_.\.' /  \  `-'    /|  | \ `'   /        | (_{;}_) | \ `"/  \  ) /  (_(=)_)
    (_I_)    |   | |  |    |  ||       .'    \       / |  |  \    /         |  (_,_)  /  '. \_/``".'    (_I_)
    '---'    '---' '--'    '--''-----'`       `'-..-'  ''-'   `'-'          /_______.'     '-----'      '---'
----------------------------------------------------------------------------------------------------------------
Automated Tinder Bot for swiping and messaging
</pre>

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## About

The Tinder Bot is a script designed to interact with the Tinder platform. It simplifies repetitive tasks such as swiping, messaging, thinking of smart openers and date setups, providing a streamlined experience for lazy fucks.

## Main features

-   **Automated Swiping**: Uses Efficientnet_b0 with a custom classifier for swiping.
-   **Auto Messaging**: Sends AI-generated messages with Gemini API.
-   **Auto Date Setup**: Sets up dates based on your date and time preferences.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/silasjul/Tinder-Bot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Tinder-Bot
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The bot requires a `.env` file to store sensitive information. Below is an example of the `.env` file:

```properties
# API key for Gemini AI (used for generating messages)
GEMINI_API_KEY=your-gemini-api-key

# Path to the Chrome user profile for Selenium
CHROME_PROFILE_PATH="C:\Users\your-username\AppData\Local\Google\Chrome\User Data"
```

### Steps to Configure:
1. Create a `.env` file in the root directory of the project.
2. Add your Gemini API key and Chrome profile path to the file.

## Usage

1. Configure your settings in the `config.json` file.
2. Ensure the `.env` file is properly set up.
3. Run the bot:
    ```bash
    python main.py
    ```

## Requirements

-   Python 3.8+
-   Selenium
-   ChromeDriver (compatible with your Chrome version)

## Disclaimer

This project is for educational purposes only. Use responsibly and ensure compliance with Tinder's terms of service.

## License

This project is licensed under the [MIT License](LICENSE).
