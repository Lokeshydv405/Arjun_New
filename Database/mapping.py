# mapping.py

# Initialize contactList (empty at first)
contactList = {}

# Function to load contactList from the file
def load_contacts():
    global contactList
    try:
        with open("contacts_data.txt", "r") as file:
            for line in file:
                name, phone = line.strip().split(",")
                contactList[name] = phone
    except FileNotFoundError:
        pass  # If no file exists, continue with an empty contactList

# Function to save contactList to the file
def save_contacts():
    with open("contacts_data.txt", "w") as file:
        for name, phone in contactList.items():
            file.write(f"{name},{phone}\n")

# Load the contacts when the script is run
load_contacts()
