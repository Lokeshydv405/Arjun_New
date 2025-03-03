import os
import tkinter as tk
from tkinter import simpledialog, messagebox

# File to save and load projects
PROJECTS_FILE = "projects_data.txt"

# Dictionary to hold project mappings
projects = {}

# Function to load projects from a file
def load_projects():
    global projects
    try:
        with open(r"C:\Users\Lokes\Desktop\Projects\Arjun_AI_4\Database\projects_data.txt", "r") as file:
            for line in file:
                name, path = line.strip().split(",")
                projects[name] = path
    except FileNotFoundError:
        pass  # If no file exists, continue with an empty projects dictionary

# Function to save projects to a file
def save_projects():
    with open(r"C:\Users\Lokes\Desktop\Projects\Arjun_AI_4\Database\projects_data.txt", "w") as file:
        for name, path in projects.items():
            file.write(f"{name},{path}\n")

# Function to open a project in VS Code
def open_in_vscode(project_name):
    """
    Opens the specified project in Visual Studio Code.
    If the project does not exist, prompts the user to add it.
    """
    load_projects()
    project_path = projects.get(project_name)

    if project_path:
        if os.path.exists(project_path):
            os.chdir(project_path)
            os.system("code .")
            return f"Opened '{project_name}' in VS Code."
        else:
            return "Error", f"The path for '{project_name}' does not exist."
    else:
        done = add_project_window(project_name)
        load_projects()
        if done:
            return open_in_vscode(project_name)
        

# Function to add a new project
def add_project(name, path):
    projects[name] = path
    save_projects()
    messagebox.showinfo("Success", f"Project '{name}' added successfully.")

# Function to update an existing project
def update_project(name):
    load_projects()
    if name in projects:
        current_path = projects[name]
        new_path = simpledialog.askstring(
            "Update Project",
            f"Current path for '{name}': {current_path}\nEnter the new path:"
        )
        if new_path:
            projects[name] = new_path
            save_projects()
            return "Success", f"Project '{name}' updated successfully."
    else:
        return "Error", f"Project '{name}' does not exist."

# Function to show all projects
def show_all_projects():
    load_projects()
    if not projects:
        return "Projects List", "No projects available."

    project_window = tk.Tk()
    project_window.title("Projects List")
    project_window.geometry("400x300")

    tk.Label(project_window, text="Projects List", font=("Arial", 16, "bold")).pack(pady=10)
    project_list_frame = tk.Frame(project_window)
    project_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for name, path in projects.items():
        tk.Label(project_list_frame, text=f"{name}: {path}", font=("Arial", 12)).pack(anchor="w", pady=2)

    tk.Button(project_window, text="Close", command=project_window.destroy).pack(pady=10)
    project_window.mainloop()

def add_project_window(project_name):
    """
    Prompts the user to enter the path for a new project if not found.
    Gracefully handles the case when the user cancels the input.
    """
    new_path = simpledialog.askstring(
        "Add Project", f"Project '{project_name}' not found. Enter the path for the project:"
    )
    if new_path is None:
        # User clicked "Cancel"
        messagebox.showinfo("Cancelled", "No project was added.")
        return False
    elif not new_path.strip():
        # User entered an empty string
        messagebox.showwarning("Input Error", "Project path cannot be empty.")
    else:
        # Valid input
        add_project(project_name, new_path)


# Function to handle project-related queries
def handle_projects(query, root):
    """
    Handle project queries like opening a project or updating its details.
    If a project is not found, it prompts to add the project.
    """
    load_projects()
    query = query.lower()  # Example: "open diet_testing in VS Code"
    project_name = query
    if 'open' in query and 'project' in query:
        project_name = project_name.replace("open ", "").replace(" in vs code", "").replace("project","").strip()
        return open_in_vscode(project_name)
    elif 'update' in query and 'project' in query and 'directory' not in query:
        project_name = project_name.replace("update ", "").replace("project","").replace("directory","").strip()
        update_project(project_name)
    elif query == "show all projects" or query == "show projects" or query == "list of my projects" or query == "show all my projects":
        show_all_projects()
    else:
        # messagebox.showerror("Error", f"Unrecognized query: '{query}'")
        return False

# Initialize Tkinter root
root = tk.Tk()
root.withdraw()  # Hide the root window, dialogs will appear as needed

# Example usage
if __name__ == "__main__":
    # Example queries
    queries = [
        "open diet_testing project in VS Code",
        "update diet_testing project",
        "show all projects"
    ]

    for query in queries:
        handle_projects(query, root)
