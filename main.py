import os
import json
import email_handler
import oauth2
import ai_handler
import time
import sys
import logging
import argparse

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_config():
    try:
        with open("settings.json") as config_file:
            config = json.load(config_file)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return None

def main():
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Run Email Auto-reader.')
        parser.add_argument('--local', action='store_true', help='Use the local AI model.')
        parser.add_argument('--try-local', action='store_true', help='Try using the local AI model first.')
        args = parser.parse_args()

        # If the --local or --try-local flag is set, override the USE_LOCAL environment variable
        if args.local or args.try_local:
            os.environ['USE_LOCAL'] = 'true'

        # Load config
        config = load_config()
        if config is None:
            sys.exit(1)

        # Connect to Gmail
        gmail_service = oauth2.get_gmail_service(config)
        if gmail_service is None:
            sys.exit(1)

        while True:
            try:
                # Get unread emails
                emails = email_handler.get_unread_emails(gmail_service)
                if emails is None:
                    continue

                # Loop through emails and mark as read if junk
                for email in emails:
                    try:
                        # Extract the email content
                        email_data = email_handler.parse_email_content(gmail_service, email)
                        if email_data is None:
                            continue

                        # Determine if email is junk using the local AI or OpenAI API
                        is_junk = ai_handler.generate_response(
                            email_data, 
                            config["ai_model"],
                            config["max_tokens"],
                            config["prompt_template"],
                            config["local_server"],
                            config["system_prompt"]
                        )

                        # Log the AI response
                        logging.info(f"AI response for email {email_data['Id']}: {is_junk}")

                        if is_junk is None:
                            continue

                        # If the email is junk, mark it as read
                        if is_junk:
                            email_handler.mark_read(gmail_service, 'me', email_data['Id'])
                            logging.info(f"Marked email {email_data['Id']} as read")

                            # If a label is specified in the settings, apply it
                            if "label" in config and config["label"]:
                                label_id = email_handler.get_label_id(gmail_service, 'me', config["label"])
                                if label_id is not None:
                                    email_handler.apply_label(gmail_service, 'me', email_data['Id'], label_id)
                                    logging.info(f"Applied label to email {email_data['Id']}")
                                else:
                                    logging.error(f"Label {config['label']} not found.")
                    except Exception as e:
                        logging.error(f"Error processing email: {e}")

            except Exception as e:
                logging.error(f"Error fetching emails: {e}")
            # Sleep for a given period specified in the configuration
            time.sleep(config["sleep_time"])
    except Exception as e:
        logging.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
