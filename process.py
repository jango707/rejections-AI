import json
from companies import comapnies

status = []

update_counter = {}

for c in comapnies:
    current_reason = ""

    with open('applications_sent.json', 'r') as file:
        data = json.load(file)
        for email in data:
            company = email["company"]
            reason = email["reason"] 
            if company == c and reason:
                current_reason= reason
        current_reason = current_reason.lower()
        if not current_reason or current_reason == "null":
            current_reason = "ghosted"

        status.append({c: current_reason})
        if current_reason not in update_counter:
            update_counter[current_reason] = 1
        else:
            update_counter[current_reason] =  update_counter[current_reason]+1
        

with open("companies_with_reason.json", 'w') as file:
    json.dump(status, file, indent=4)
with open("top_reasons.json", 'w') as file:
    json.dump(update_counter, file, indent=4)