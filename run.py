import os
# import eel
# # from Basic_Utilities.TakeCommand import *
# # from engine.features import *
# # from engine.command import *
# # from engine.auth import recoganize
# # def start():
# print("Hello")
# eel.init("FrontEnd2")



# print("Hello")
# eel.start('index.html', mode=None, host='localhost',port=5500, block=False)
# print("Hello")
#     # playAssistantSound()
#     # @eel.expose
#     # def init():
#     #     subprocess.call([r'device.bat'])
#     #     eel.hideLoader()
#     #     speak("Ready for Face Authentication")
#     #     flag = recoganize.AuthenticateFace()
#     #     if flag == 1:
#     #         eel.hideFaceAuth()
#     #         speak("Face Authentication Successful")
#     #         eel.hideFaceAuthSuccess()
#     #         speak("Hello, Welcome Sir, How can i Help You")
#     #         eel.hideStart()
#     #         playAssistantSound()
#     #     else:
            # speak("Face Authentication Fail")

# # eel.start('index.html', mode=None, host='localhost', block=True)

import eel
from Basic_Utilities.TakeCommand import takecommand
from Basic_Utilities.General_functions import greet
from Basic_Utilities.say import say
from main import totalcontrol
# Initialize the front-end folder
eel.init("FrontEnd2")  # Make sure the folder name is correct

# Start the app
try:
    # os.system('start msedge.exe --app="http://localhost:5500/FrontEnd2/index.html"')
    eel.start('index.html', mode='chrome', host='localhost', port=5500, block=False)
    say(greet())
    print("Eel application started successfully.")
except Exception as e:
    print(f"Error starting Eel application: {e}")

# Keep the Python process running
while True:
    eel.sleep(1)
