import subprocess
import webbrowser
import os
import time

def start_Server():
       server_process = subprocess.Popen(["python", "TodoList/app.py"], shell=True)
       return server_process
   
def open_todo_list():
    # Start the Flask server

    # Wait a few seconds for the server to start
    time.sleep(3)
    
    # Path to the index.html file
    html_path = os.path.abspath("TodoList/templates/list_frontend.html")
    # Open the index.html in the default web browser
    webbrowser.open(f"http://127.0.0.1:5000/")
    
    return  # Return the process in case you want to close it later

def stop_todo_list(server_process):
    server_process.terminate()
    print("To-Do List server stopped.")




# Example call
# This should be called based on Arjun's recognized prompt
# open_todo_list()
# time.sleep(10)
# stop_todo_list()