import json

# Load the JSON file
with open('1679946434.json', 'r') as f:
    data = json.load(f)

# Loop through each article in the list
for article in data:
    # Access the article content
    article_content = article['content']

    # Print the article content
    print(article_content)

