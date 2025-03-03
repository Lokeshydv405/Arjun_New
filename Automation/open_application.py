import os
import webbrowser
import random
from Basic_Utilities.say import say
from Database.openapplications import app_opening_dialogues, website_opening_dialogues

# Define applications and websites with their paths or URLs
applications = {
    'whatsapp': "start whatsapp:",
    'excel': "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE",
    'powerpoint': "C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE",
    'google chrome': "C:/Program Files/Google/Chrome/Application/chrome.exe",
    'camera': "start ms-camera:",
    'calendar': "start outlookcal:",
    'canva': "https://www.canva.com/"
}

websites = {
    'youtube': 'https://www.youtube.com/',
    'wikipedia': 'https://www.wikipedia.com/',
    'lms': 'https://lms.iitmandi.ac.in/',
    'google': 'https://www.google.com/',
    'linkedin': 'https://www.linkedin.com/',
    'github': 'https://github.com/',
}

search_phrases = [
    "search for", "look up", "find", "google", "look for", "get info on",
    "show me", "find details on", "pull up information on", "give me info on",
    "fetch details for", "tell me about", "I want to know about",
    "can you look up", "I'd like to find", "help me search for",
    "show details on", "find out about", "look into", "explore"
]

# Open Applications based on user query
def Open_Apps(query):
    for app_name, app_path in applications.items():
        if f"open {app_name}" in query.lower():
            if app_path.startswith("http"):
                webbrowser.open(app_path)
            else:
                os.system(f'"{app_path}"')
            
            to_say = random.choice(app_opening_dialogues.get(app_name, [f"Opening {app_name}"]))
            print(to_say)
            # say(to_say)
            return to_say
    return False

# Open Websites based on user query
def Open_websites(query):
    for site_name, site_url in websites.items():
        if f"open {site_name}" in query.lower():
            if 'google' in query.lower() and 'chrome' in query.lower():
                continue

            search_query = None
            for phrase in search_phrases:
                if phrase in query.lower():
                    search_query = query.lower().split(phrase, 1)[1].strip()
                    break

            url = site_url + (search_query if search_query else "")
            webbrowser.open(url)
            
            if search_query:
                to_say = f"Opening {site_name} and searching for {search_query}"
            else:
                to_say = random.choice(website_opening_dialogues.get(site_name, [f"Opening {site_name}"]))
            
            print(to_say)
            # say(to_say)
            return to_say
    return False

def Open_Applications(query):
    response = Open_websites(query)
    if response:
        return response
    response = Open_Apps(query)
    if response:
        return response
# Example usage
if __name__ == "__main__":
    app_query = "open Excel"
    site_query = "open YouTube"

    if not Open_Apps(app_query):
        Open_websites(site_query)
    # os.system("start googlechrome:")
