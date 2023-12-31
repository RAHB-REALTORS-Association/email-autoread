# ✉️ Email AntAI-Spam 🤖

[![Continuous Integration](https://github.com/RAHB-REALTORS-Association/email-autoread/actions/workflows/python-app.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/email-autoread/actions/workflows/python-app.yml)
[![Docker Image](https://github.com/RAHB-REALTORS-Association/email-autoread/actions/workflows/docker-image.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/email-autoread/actions/workflows/docker-image.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Email AntAI-Spam ✉️🤖 is a Python tool that uses AI to automatically mark as read any unread Gmail messages that are likely to be junk, and optionally apply a label to them. This streamlines email management tasks by reducing the amount of junk mail you need to manually filter. It can use either a local AI model or the OpenAI API based on your configuration.

## Table of Contents
- [🐳 Running with Docker](#running-with-docker)
- [🛠️ Manual Setup](#%EF%B8%8F-manual-setup)
- [❓ How it works](#-how-it-works)
- [🧾 Logging](#-logging)
- [📝 Note](#-note)
- [🌐 Community](#-community)
  - [Contributing 👥🤝](#contributing-)
  - [Reporting Bugs 🐛📝](#reporting-bugs-)
- [📄 License](#-license)

## 🐳 Running with Docker

To get started, you first need to pull the Docker image from the GitHub Container Registry. You can do this by running the following command in your terminal:

```bash
docker pull ghcr.io/rahb-realtors-association/email-autoread:latest
```

You need to provide your OpenAI API key and specify whether you want to use a local AI model or the OpenAI API. You also need to bind mount your `settings.json` file into the Docker container. 

You can do this by running the following command:

```bash
docker run -e OPENAI_API_KEY=<your_openai_api_key> -v /path/to/your/settings.json:/app/settings.json -v /path/to/your/credentials.json:/app/credentials.json -v /path/to/your/tocken.pickle:/app/token.pickle ghcr.io/rahb-realtors-association/email-autoread:latest
```

Please replace `<your_openai_api_key>` with your actual OpenAI API key, `/path/to/your/settings.json` with the actual path to your `settings.json` file on your host system, and the same for `credentials.json` and `token.pickle`.

## 🛠️ Manual Setup

1. Clone this repository to your local machine:
```bash
git clone https://github.com/RAHB-REALTORS-Association/email-autoread.git
cd email-autoread
```
3. Install the required Python packages by running the following command in your terminal:
```bash
pip install -r requirements.txt
```
3. Set up a project in the Google API Console, enable the Gmail API, and download the `credentials.json` file. For detailed instructions, please refer to the [Google API Python Client's User Guide](https://googleapis.github.io/google-api-python-client/docs/).
4. Place the `credentials.json` file in the same directory as your Python script.
5. Adjust the settings in `settings.json` to match your setup. You can specify the AI model and the Gmail scopes.
6. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
7. Set the `USE_LOCAL` environment variable to `true` if you want to use a local AI model, or `false` (or leave it unset) if you want to use the OpenAI API.
8. Run the script by executing the following command in your terminal:
```bash
python main.py
```

You can also add the `--local` flag to use the local AI model, regardless of the `USE_LOCAL` environment variable:

```bash
python main.py --local
```

## ❓ How it works

The script performs the following steps in a loop:

1. Connects to Gmail using OAuth 2.0. 🔒
2. Fetches unread emails. 📥
3. Parses the email content. 📝
4. Sends the email content to either a local AI model or the OpenAI API, based on your configuration, to determine if the email is likely to be junk. 📧🤖🔍
5. If the email is determined to be junk, it is marked as read and, if specified in the settings, a label is applied. 👀🗑️🏷️

The script sleeps for an hour between each loop.

## 🧾 Logging

The script logs information and error messages to a file named `app.log`. This can be used to monitor the script's operation and troubleshoot any issues.

## 📝 Note

This script is intended to be run locally on a user's machine. The user must be able to open a web browser on the machine to authorize the script with their Google account.

Please note that the AI's judgement might not be perfect, and you may need to do some fine-tuning of the AI prompts, the interpretation of the AI's responses, or other parts of the code to get the best results. Testing and iteration will likely be needed to achieve the best performance.

## 🌐 Community

### Contributing 👥🤝

Contributions of any kind are very welcome, and would be much appreciated. For Code of Conduct, see [Contributor Convent](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

To get started, fork the repo, make your changes, add, commit and push the code, then come back here to open a pull request. If you're new to GitHub or open source, [this guide](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3#let-s-make-our-first-pull-request-) or the [git docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) may help you get started, but feel free to reach out if you need any support.

[![Submit a
PR](https://img.shields.io/badge/Submit_a_PR-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/email-autoread/compare)

### Reporting Bugs 🐛📝

If you've found something that doesn't work as it should, or would like to suggest a new feature, then go ahead and raise an issue on GitHub. For bugs, please outline the steps needed to reproduce, and include relevant info like system info and resulting logs.

[![Raise an
Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/email-autoread/issues/new/choose)

## 📄 License
This project is open sourced under the MIT license. See the [LICENSE](LICENSE) file for more info. 📜
