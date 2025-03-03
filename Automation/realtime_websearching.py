import requests
apikey = 'AIzaSyA5djFSdnsMCCo9vsMBLCc7lYaWo4ByTd8'
cx = 'a4ba07d92aa88488f'
# <script async src="https://cse.google.com/cse.js?cx=a4ba07d92aa88488f">
# </script>
# <div class="gcse-search"></div>
def real_time_web_search(query,cx,apikey):
    print(apikey)
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={apikey}&cx={cx}'

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('items', [])
        if results:
            result = results[0]
            print(f"Title: {result['title']}")
            print(f"Snippet: {result['snippet']}")
            print(f"Link: {result['link']}\n")
            return [result['snippet'],result['link']]
        else:
            print("No results found.")
    else:
        print(f"Error: {response.text}")
        print(f"Error: {response.status_code}")


def is_web_search_query(query):
    # Simple heuristic to determine if a query is a web search query
    web_search_keywords = ['how', 'what', 'why', 'who', 'where', 'when', 'search', 'find', 'google', 'current','currently','nowerdays','now']
    return any(keyword in query.lower() for keyword in web_search_keywords)

def main_real_web_search(query):
    if is_web_search_query(query):
        output = real_time_web_search(query,cx,apikey)
        return f"{output[0]}"
    else:
        return False
