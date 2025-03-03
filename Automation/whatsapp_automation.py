import pywhatkit
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from Basic_Utilities.say import say
contactList = {}

# Function to load contactList from the file
def load_contacts():
    global contactList
    try:
        with open(r"C:\Users\Lokes\Desktop\Projects\Arjun_AI_4\Database\contacts_data.txt", "r") as file:
            for line in file:
                name, phone = line.strip().split(",")
                contactList[name] = phone
    except FileNotFoundError:
        print("No file")
        pass  # If no file exists, continue with an empty contactList

# Function to save contactList to the file
def save_contacts():
    try:
        with open(r"C:\Users\Lokes\Desktop\Projects\Arjun_AI_4\Database\contacts_data.txt", "w") as file:
            for name, phone in contactList.items():
                file.write(f"{name},{phone}\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        pass
    

# Contact management functions
def search_contact(name):
    load_contacts()  # Load contacts before searching
    return contactList.get(name, False)

def add_contact(name, phone):
    contactList[name] = phone
    save_contacts()  # Save the updated contactList to the file
    return phone

# WhatsApp-related functions
def send_whatsapp_message(phone_number, message, time=None):
    """
    Send a message to a specific phone number at a specified time.
    If no time is provided, send the message instantly.
    """
    try:
        if time is None:
            pywhatkit.sendwhatmsg_instantly(phone_number, message, tab_close=False)
        else:
            pywhatkit.sendwhatmsg(phone_number, message, time[0], time[1])
        return "Message sent successfully."
    except Exception as e:
        return f"An error occurred: {e}"

def contacts(name):
    """
    Search for a contact and handle addition or update.
    This function will show the contact input window if the contact is not found.
    """
    result = search_contact(name)

    if result:
        return result
    else:
        return None

def extract_phone_and_message(query, root):
    """
    Extract phone number and message from the query.
    """
    try:
        if "send message" in query:
            name_or_number = query.split("to")[-1].strip()
            message = query.split("message")[1].split("to")[0].strip()

            if name_or_number.startswith("+"):
                phone_number = name_or_number
            else:
                phone_number = contacts(name_or_number)  # Handle contact lookup or addition
                if not phone_number:# If contact is not found, show the input window
                    say(f"Contact '{name_or_number}' not found. Enter the phone number to add {name_or_number}:")
                    phone_number = request_contact_info(root, name_or_number)

            return phone_number, message
        else:
            raise ValueError("Invalid query format.")
    except Exception as e:
        return None, f"Error parsing query: {e}"

def handlewhatsapp(query, root):
    """
    Handle the query to send a WhatsApp message.
    This will only trigger the window for contact input when necessary.
    """
    phone_number, message = extract_phone_and_message(query, root)

    if phone_number and message:
        response = send_whatsapp_message(phone_number, message)
        return response
    else:
        return False

# Function to request contact information
def request_contact_info(root, name):
    """
    This function will prompt the user for the phone number of the contact if it's not found.
    It will show a Tkinter dialog to ask for the phone number.
    """
    phone = simpledialog.askstring("Input", f"Contact '{name}' not found. Enter the phone number to add {name}:")
    if phone:
        add_contact(name, phone)  # Add the new contact to the list and save it
        messagebox.showinfo("Success", f"Contact {name} added successfully.")
        return phone
    else:
        messagebox.showwarning("Input Error", "Phone number cannot be empty.")
        return None

# Initialize Tkinter window immediately
root = tk.Tk()
root.withdraw()  # Hide the root window, will show dialogs only when needed

# # Main function for testing
if __name__ == "__main__":
    print(contactList)
    load_contacts()  # Load contacts when the script starts
    # save_contacts()
    query = "send message hello to D"
    response = handlewhatsapp(query, root)
    print(response)



