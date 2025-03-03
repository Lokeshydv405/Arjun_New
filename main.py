import os
import webbrowser
import datetime
import eel
import tkinter as tk
from pytube import Search
from Automation.projects_open import handle_projects
from Automation.realtime_websearching import main_real_web_search
from Chatting.Chat import chat
from Automation.open_application import Open_Applications
from Basic_Utilities.AI_Prompts import AI_Prompt_Writing
from Basic_Utilities.say import say        
from Basic_Utilities.General_functions import greet, Exit, handle_query_wt
from Basic_Utilities.TakeCommand import takecommand
from Automation.search_control import handle_query
from Automation.youtube_automation import command_handler
from ToDoList.TaskControl import ToDOmain
from Automation.whatsapp_automation import handlewhatsapp
from Database.onstart_db import wake_up_phrases
# from Databse.mapping import add_contact,update_contact

# Initialize global states
youtube_mode = False
global speek 
global revert 
revert = False
@eel.expose
def totalcontrol(message=1):
    """
    Handle user input (voice or text) and return the response.
    """
    global youtube_mode
    final_response = None  # Variable to hold the final response
    speek = True
    root = tk.Tk()
    root.withdraw() 
    if message == 1:
        query = takecommand()
    else:
        query = message

    eel.senderText(query)  # Send the user query to the frontend
    if query:
        query = query.lower() 
        # Handle YouTube Mode
        if 'enter youtube' in query:
            say("Entering YouTube mode")
            youtube_mode = True
            final_response = "Entering YouTube mode"

        elif 'exit youtube' in query:
            say("Exiting YouTube mode")
            youtube_mode = False
            final_response = "Exiting YouTube mode"

        elif youtube_mode:
            command_handler(query)
            final_response = "Command executed in YouTube mode"

        else:
            # Evaluate all functions once and store their results
            # web_search_response = main_real_web_search(query)
            whatsapp_response = handlewhatsapp(query,root)
            project_response = handle_projects(query,root)
            handle_query_wt_result = handle_query_wt(query)
            handle_query_result = handle_query(query)
            open_applications_result = Open_Applications(query)
            todo_result = ToDOmain(query)

            # Check the results
            if handle_query_wt_result:
                final_response = handle_query_wt_result
            elif open_applications_result:
                final_response = open_applications_result
            elif handle_query_result:
                final_response = handle_query_result
            elif whatsapp_response:
                final_response = whatsapp_response
            elif project_response:
                final_response = project_response
            elif 'make a file and write' in query:
                AI_Prompt_Writing(query)
                final_response = "Done, check for the file in the Answers folder."
            elif todo_result:
                final_response = todo_result
            # elif web_search_response:
                # final_response = web_search_response
            else:
                # Chat Handling (default fallback)
                is_code, chat_response = chat(query)
                final_response = chat_response
                speek = not is_code  # Speak only if no code is detected

    else:
        say("Sorry, I didn't understand that. Please try again.")
        final_response = "Sorry, I didn't understand that. Please try again."

    eel.receiverText(final_response)  # Send the final response to the frontend
    if speek:
        say(final_response)
    return final_response


if __name__ == '__main__':
    # Wake-up functionality is commented out but retained for future use.
    # while not wake:
    #     print("Arjun is offline")
    #     query = takecommand()
    #     if query:
    #         query = query.lower()
    #         wake = WakeUp_function(query)
    #         if wake:
    #             print("Arjun is online now")
    #             greet()

    print("Arjun is online")
    greet()

    while True:
        query = takecommand()
        if query:
            totalcontrol(query)
