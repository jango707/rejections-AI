
import json
import requests
import MboxReader
import email
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime

import re

def remove_https_links(text):
    # Define a regular expression pattern for matching https links
    pattern = r'https://\S+'
    pattern2 = r'http://\S+'
    # Use re.sub to replace the links with an empty string
    cleaned_text = re.sub(pattern, '', text)
    cleaned_text = re.sub(pattern2, '', text)
    return cleaned_text

# Function to extract content from raw email
def extract_email_content(raw_email):
    # Parse the raw email
    email_message = email.message_from_string(raw_email, policy=policy.default)
    email_date = email_message['Date']

    # Initialize variables to store email parts
    text_content = ""

    # Walk through the email parts
    for part in email_message.walk():
        content_type = part.get_content_type()
        disposition = part.get("Content-Disposition")

        if content_type == "text/plain" and disposition is None:
            text_content += part.get_payload(decode=True).decode(part.get_content_charset())

    return remove_https_links(text_content), email_date





with MboxReader.MboxReader("data.mbox") as mbox:

    rejections = []
    sys_prompt = "I have been applying for jobs for a Software Engineering position. I provide you with an email content. Tell me if it is a rejection email or not for a role that I applied to. If it is a rejection email, give me the company name and a short (3 words) reason why.Give me the response in this format: {\"rejection\": true/false, \"company\": \"name of company\", \"reason\": \"reason for rejection\" } only include the company details when it is a rejection, otherwise just return the first line of the json."

    for message in mbox: 

        text_content, email_date = extract_email_content(message.as_string())
        year = parsedate_to_datetime(email_date).year
        if year != 2024: 
            break
        print("length: " + len(text_content))

        if len(text_content) > 40000:
            print("too large...")
            continue

        headers = {"Authorization": "Bearer PRIVATE"}

        url = "https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "perplexityai/llama-3-sonar-small-32k-chat",
            "text": text_content + ".",
            "chatbot_global_action": sys_prompt,
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 150,
        }

        response = requests.post(url, json=payload, headers=headers)

        result = json.loads(response.text)
        print(result)

        jsonResult =json.loads(result['perplexityai/llama-3-sonar-small-32k-chat']['generated_text'])
        isRejection = jsonResult["rejection"] # True or False
        print(jsonResult)


        if isRejection:
            company = jsonResult["company"]  
            reason = jsonResult["reason"]  
            rejections.append({"company": company, "reason": reason})


    with open("test.json", 'w') as file:
        json.dump(rejections, file, indent=4)

        