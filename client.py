import requests
from bs4 import BeautifulSoup

def get_wikipedia_summary(query):
    # Replace spaces in query with underscores for Wikipedia URL format
    query = query.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract paragraphs
        paragraphs = soup.find_all('p')
        summary = []

        # Limit to the first 2 paragraphs for a brief summary
        for i, paragraph in enumerate(paragraphs[:2]):
            summary.append(paragraph.get_text())

        return "\n".join(summary) if summary else "No relevant information found."
    else:
        return "Failed to retrieve information."

def main():
    answer = "who is Hrithik Roshan"
    phrases_to_remove = ["what is","who is", "who are", "where is", "when is", "how is", "why is", "what are", "who were"]
    query_lower = answer.lower()
    for phrase in phrases_to_remove:
        if query_lower.startswith(phrase):
            answer =  answer[len(phrase):].strip()

    
    print(answer)
    answer = get_wikipedia_summary(answer)
    print(answer)
main()