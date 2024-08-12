## Requirements

- Python 3.7+
- OpenAI API Key
- Slack Bot Token
- Slack Signing Secret

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/conversational_ai.git
   cd conversational_ai

## How to Use the README

1. **Clone the Repository**: Provide the actual URL of your repository in the `git clone` command.
2. **Set Up Environment Variables**: Make sure to replace `'your_openai_api_key'`, `'your_slack_bot_token'`, and `'your_slack_signing_secret'` with your actual keys.
3. **Run the Script**: Follow the instructions to run the script and set up the Slack app.
    1. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

    2. Set up environment variables:

    ```sh
    export OPENAI_API_KEY='your_openai_api_key'  
    export SLACK_BOT_TOKEN='your_slack_bot_token'  
    export SLACK_SIGNING_SECRET='your_slack_signing_secret'
    ```

## Usage

```sh
python main.py
```

## Set Up Your Slack App

### Create a Slack App

1. Go to the Slack API page.
2. Click on the "Create New App" button.
3. Choose "From scratch" and give your app a name, then select the workspace where you want to install the app.
4. Click "Create App".

### Enable the Events API

1. In your app's settings, navigate to the "Event Subscriptions" section.
2. Toggle the "Enable Events" switch to "On".
3. In the "Request URL" field, enter `http://your_server:3000/slack/events`. Replace `your_server` with your server's actual address (e.g., `http://localhost:3000` for local testing or your deployed server's URL).
4. Click "Save Changes".

### Subscribe to Bot Events

1. In the "Event Subscriptions" section, scroll down to the "Subscribe to Bot Events" section.
2. Click "Add Bot User Event".
3. Add the `message.channels` event. This event will allow your bot to listen to messages in channels where it is invited.
4. Click "Save Changes".

### Enable OAuth & Permissions

1. Navigate to the "OAuth & Permissions" section in your app's settings.
2. Under "Scopes", add the following bot token scopes:
   - `channels:history` - to read messages in channels.
   - `files:read` - to read files uploaded to channels.
   - `chat:write` - to send messages to channels.
3. Click "Save Changes".

### Install the App to Your Workspace

1. In the "OAuth & Permissions" section, scroll up to the "OAuth Tokens for Your Workspace" section.
2. Click the "Install App to Workspace" button.
3. Follow the prompts to authorize the app in your workspace.
4. After installation, you will receive a "Bot User OAuth Access Token". Copy this token and set it as the `SLACK_BOT_TOKEN` environment variable.

### Set Up the Signing Secret

1. Navigate to the "Basic Information" section in your app's settings.
2. Scroll down to the "App Credentials" section.
3. Copy the "Signing Secret" and set it as the `SLACK_SIGNING_SECRET` environment variable.

### Invite the Bot to a Channel

1. In your Slack workspace, invite the bot to a channel by typing `/invite @your_bot_name` in the channel where `your_bot_name` is the name of your bot.

### Upload a PDF File and Ask a Query

1. In the channel where the bot is invited, upload a PDF file.
2. In the same message or a subsequent message, ask a query related to the content of the PDF file.
   - The bot will process the PDF, extract the text, store it in the vector database, retrieve relevant chunks based on your query, and use OpenAI's GPT-4 to generate an answer. The bot will then post the answer in the Slack channel.
