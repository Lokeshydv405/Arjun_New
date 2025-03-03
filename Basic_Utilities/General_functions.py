import datetime
from config import WeatherAPI
from Basic_Utilities.say import say
import requests
from Basic_Utilities.geolocation import get_location_details
# from Chatting.Chat import chat
from Database.onstart_db import greeting,time_phrases,weather_phrases,quit_phrases,goodbye_greetings
import random

def get_weather_info(city = "Mandi", state = "HimachalPradesh", country = 'India'):
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?id=1263862&exclude=hourly,daily&appid={WeatherAPI}&q={city},{state},{country}"
    response = requests.get(base_url)
    weather_data = response.json()
    # print(weather_data)
    if weather_data['cod'] != '404':
        y = weather_data["list"][0]
        temp = y['main']
        current_temperature = round(temp["temp"] - 273.15, 1)  # Convert from Kelvin to Celsius
        weather_description = y["weather"][0]["description"].capitalize()

        return f"It's currently {current_temperature} degrees Celsius with {weather_description}."
    else:
        return "I'm having trouble fetching the current weather."

def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM
    return f"The time is {current_time}."

def greet():
    current_hour = datetime.datetime.now().hour

    if 5 <= current_hour < 12:
        greet_message = greeting('morning')
    elif 12 <= current_hour < 17:
        greet_message = greeting('afternoon')
    elif 17 <= current_hour < 21:
        greet_message = greeting('evening')
    else:
        greet_message = greeting('night_working')
    print(greet_message, end='\n')
    say(greet_message)

def handle_query_wt(query):
    for i in time_phrases:
        if i.lower() in query.lower():
            time_message = get_time()
            # say(time_message)
            # print(time_message)
            return time_message
        
    # for i in weather_phrases_Locations:
    #     if i.lower() in query.lower():
    #         weather_info = get_weather_info()
    #         say(weather_info)
    #         print(weather_info)
    #         return True
    
    for i in weather_phrases:
        if i.lower() in query.lower():
            # city, state, country = get_location_details()
            # print(city,state,country)
            weather_info = get_weather_info()
            # say(weather_info)
            # print(weather_info)
            return weather_info


def Exit(query):
    for phrase in quit_phrases:
        if phrase.lower() in query.lower():
            to_say = random.choice(goodbye_greetings)
            print(to_say)
            print()
            say(to_say)
            return True
    return False
