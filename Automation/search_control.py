import webbrowser
import re
from youtubesearchpython import VideosSearch
from Basic_Utilities.say import say
from Basic_Utilities.TakeCommand import takecommand

commands = {
    'music': 'Which music would you like to listen to today?',
    'video': 'Which video would you like to watch today?',
    'movie': 'Which movie would you like to watch today?',
    'podcast': 'Which podcast would you like to listen to today?',
    'search': 'What would you like to search for on Google?',
}

media_keywords = {
    'music': ['listen to', 'play', 'music', 'song', 'track', 'album', 'genre'],
    'video': ['watch', 'play', 'video', 'clip'],
    'movie': ['watch', 'movie', 'film'],
    'podcast': ['listen to', 'play', 'podcast', 'episode'],
}

search_keywords = ['google', 'search for', 'look up', 'find', 'search about']

def extract_details(query):
    patterns = [
        r'listen to (?P<detail>.+)',
        r'play (?P<detail>.+)',
        r'watch (?P<detail>.+)',
        r'I want to listen to (?P<detail>.+)',
        r'I want to watch (?P<detail>.+)',
        r'I would like to listen to (?P<detail>.+)',
        r'I would like to watch (?P<detail>.+)',
        r'search for (?P<detail>.+)',
        r'google (?P<detail>.+)',
        r'find (?P<detail>.+)',
        r'look up (?P<detail>.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group('detail').strip()
    return None

def play_media(media_type, name):
    # say(f"Searching for {name} on YouTube...")
    search = VideosSearch(name, limit=1)
    search_results = search.result()
    if search_results['result']:
        first_result = search_results['result'][0]
        video_url = first_result['link']
        webbrowser.open(video_url)
        # say(f"Playing {name} for you")
        return f"Playing {name} for you"
    else:
        say("Sorry, I couldn't find that on YouTube.")
        return f"Couldn't find {name} on YouTube."

def search_google(query):
    # say(f"Searching for {query} on Google...")
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    return f"Searching for {query} on Google..."

def handle_query(query):
    query_lower = query.lower()

    # Check for media commands
    for media_type, keywords in media_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            specific_detail = extract_details(query)
            
            if not specific_detail:
                say(commands[media_type])
                specific_detail = takecommand().lower()
            
            return play_media(media_type, specific_detail)

    # Check for search commands
    if any(keyword in query_lower for keyword in search_keywords):
        specific_detail = extract_details(query)
        
        if not specific_detail:
            say(commands['search'])
            specific_detail = takecommand().lower()
        
        return search_google(specific_detail)

    # No matching command
    return False

# Example usage
if __name__ == "__main__":
    query = "search for the weather today"  # Replace this with user input
    result = handle_query(query)
    if result:
        print(result)  # Log or display the response for the chatbox
