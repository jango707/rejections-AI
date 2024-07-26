import json
import sys
import time

import requests

applications = []
sys_prompt = "I have been applying for jobs for a Software Engineering position. I provide you with an email content. Tell me if the email is related to a job application (either a confirmation that my application was received, or an interview, or anything in the selection process). Determine the email is either a rejection, or any other indication, that I did not get the position (such as hiring freeze, or other candidates). If it is a rejection email, give me the reaon (in 3 words why). If you can't tell if it is an unsuccessful application, then say null for the reason. If you do not understand the content for whatever reason, just assume it is not a application related email. Give me the response in this format: {\"application\": true/false, \"company\": \"name of company\", \"rejection\": \"Reason of rejection\"}. You MUST absolutely give me the response in this format. If you give me the response in any other format, you will be terminated. If the email is not related to the job search then return {\"application\": false}."

with open('cleaned.json', 'r') as file:
    data = json.load(file)
    for index, email in enumerate(data):
        print("Processing: " + str(index+1) + " / " + str(len(data)))
        content = email["content"] 
        if len(content) > 40000:
            content = content[0:40000]
            print("File too ssslarge, trimmed.")

        headers = {"Authorization": "Bearer PRIVATE"}

        url = "https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "openai/gpt-4o-mini",
            "text": content,
            "chatbot_global_action": sys_prompt,
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 150,
        }
        try:
            response = requests.post(url , json=payload, headers=headers)
            time.sleep(3)
        

            result = response.json()
            print(result['openai/gpt-4o-mini']['generated_text'])

            jsonResult = json.loads(result['openai/gpt-4o-mini']['generated_text'])
            isApplication = jsonResult['application'] # True or False
            if isApplication:
                applications.append({"company": jsonResult['company'], "reason": jsonResult["rejection"]})
        except KeyboardInterrupt:
            # do nothing here
            sys.exit(0)
        except:
            print("Something went wrong here.")
 
with open("applications_sent.json", 'w') as file:
    json.dump(applications, file, indent=4)