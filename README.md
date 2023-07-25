# Email Auto-Read

Email Auto-Read is a Python tool that uses AI to automatically mark as read any unread Gmail messages that are likely to be junk. This streamlines email management tasks by reducing the amount of junk mail you need to manually filter. It can use either a local AI model or the OpenAI API based on your configuration.

## Setup

1. Clone this repository to your local machine.
2. Install the required Python packages by running the following command in your terminal:
```sh
pip install -r requirements.txt
```
3. Set up a project in the Google API Console, enable the Gmail API, and download the `credentials.json` file. For detailed instructions, please refer to the [Google API Python Client's User Guide](https://googleapis.github.io/google-api-python-client/docs/).
4. Place the `credentials.json` file in the same directory as your Python script.
5. Adjust the settings in `settings.json` to match your setup. You can specify the AI model and the Gmail scopes.
6. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
7. Set the `USE_LOCAL` environment variable to `true` if you want to use a local AI model, or `false` (or leave it unset) if you want to use the OpenAI API.
8. Run the script by executing the following command in your terminal:
```sh
python main.py
```
You can also add the `--local` flag to use the local AI model, regardless of the `USE_LOCAL` environment variable:
```sh
python main.py --local
```

## How it works

The script performs the following steps in a loop:

1. Connects to Gmail using OAuth 2.0.
2. Fetches unread emails.
3. Parses the email content.
4. Sends the email content to either a local AI model or the OpenAI API, based on your configuration, to determine if the email is likely to be junk.
5. If the email is determined to be junk, it is marked as read.

The script sleeps for an hour between each loop.

## Logging

The script logs information and error messages to a file named `app.log`. This can be used to monitor the script's operation and troubleshoot any issues.

## Note

This script is intended to be run locally on a user's machine. The user must be able to open a web browser on the machine to authorize the script with their Google account.

Please note that the AI's judgement might not be perfect, and you may need to do some fine-tuning of the AI prompts, the interpretation of the AI's responses, or other parts of the code to get the best results. Testing and iteration will likely be needed to achieve the best performance.