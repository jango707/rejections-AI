
import json
import requests
import MboxReader
import email
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
import time

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
    email_author = email_message['from']

    text_content = ""
 
    for part in email_message.walk():
        content_type = part.get_content_type() 

        if content_type == "text/plain":
            text_content += part.get_payload()  

    return remove_https_links(text_content), email_date, email_author





with MboxReader.MboxReader("data.mbox") as mbox:

    rejections = []
    sys_prompt = "I have been applying for jobs for a Software Engineering position. I provide you with an email content. Tell me if the email comes from a company that I applied for and the application was unsuccessful. An unsuccesful application means that I did not get the job, if the hiring process is on hold, then that is unsuccesful. If it is a rejection email or the application was unsuccuesful, give me the company name and a short (3 words) reason why. Give me the response in this format: {\"rejection\": true/false, \"company\": \"name of company\", \"reason\": \"reason for rejection\" } only include the company details when it is a rejection, otherwise just return the first line of the json."

    print("Processing...")
    for i, message in enumerate(mbox):
        text_content, email_date, author = extract_email_content(message.as_string())
        if email_date is not None:
            if email_date == "22-10-22 ":
                continue    
            year = parsedate_to_datetime(email_date.strip()).year
            if year != 2024: 
                continue
        else:
            email_date = "???"
        #print("length: " + str(len(text_content)))
        
        #     continue
        # if len(text_content) > 40000:
        #     print("too large...")
        #     continue

        rejections.append({
            "date": email_date,
            "content": text_content,
            "author": author
        })
        print("Emails so far in 2024: " + str(len(rejections)))

        headers = {"Authorization": "Bearer PRIVATE"}

        url = "https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "openai/gpt-4o-mini",
            "text": text_content + ".",
            "chatbot_global_action": sys_prompt,
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 150,
        }

        # response = requests.post(url, json=payload, headers=headers)

        # result = json.loads(response.text)
        # print(result)

        # jsonResult =json.loads(result['openai/gpt-4o-mini']['generated_text'])
        # isRejection = jsonResult["rejection"] # True or False
        # print(jsonResult)


        # if isRejection:
        #     company = jsonResult["company"]  
        #     reason = jsonResult["reason"]  
        #     rejections.append({"company": company, "reason": reason})

        # time.sleep(5) 
        

    print(len(rejections))
    with open("test.json", 'w') as file:
        json.dump(rejections, file, indent=4)

        