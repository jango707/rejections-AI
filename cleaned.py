import json
more_cleaned = []
with open('test.json', 'r') as file:
    data = json.load(file)
    for index, email in enumerate(data):
        date = email["date"]
        author = email["author"]
        content = email["content"]
        if content != "" and date != "???" and "jangbel" not in author and author is not None:
            more_cleaned.append(email)

print(len(more_cleaned))
with open("cleaned.json", 'w') as file:
    json.dump(more_cleaned, file, indent=4)