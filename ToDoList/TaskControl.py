# from Database.ToDoList_db import *
from ToDoList.app import add_task_db,get_tasks_db
from ToDoList.main_todolist import start_Server, open_todo_list, stop_todo_list
import datetime
import re

def parse_date(date_str):
    """
    Convert text-based dates like 'today', 'tomorrow', '16th April' to a valid date format (YYYY-MM-DD).
    """
    today = datetime.date.today()

    # Handle relative days
    if date_str in ["today", "todays", "now"]:
        return today.strftime("%Y-%m-%d")
    elif date_str in ["tomorrow", "tommorow"]:
        return (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str in ["day after tomorrow"]:
        return (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    # Handle dates like '16th April' or 'April 16'
    date_match = re.search(r"(\d{1,2})(st|nd|rd|th)?\s*(\w+)", date_str, re.IGNORECASE)
    if date_match:
        day = int(date_match.group(1))
        month_str = date_match.group(3)
        try:
            month = datetime.datetime.strptime(month_str, "%B").month  # Full month name
        except ValueError:
            try:
                month = datetime.datetime.strptime(month_str, "%b").month  # Short month name
            except ValueError:
                return today.strftime("%Y-%m-%d")  # Default to today if month is unrecognized
        return datetime.date(today.year, month, day).strftime("%Y-%m-%d")

    # Handle numeric dates like "16/04/2025" or "16-04-2025"
    numeric_date_match = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", date_str)
    if numeric_date_match:
        day, month, year = map(int, numeric_date_match.groups())
        return datetime.date(year, month, day).strftime("%Y-%m-%d")

    return today.strftime("%Y-%m-%d")  # Default fallback

def extract_task_and_date(query):
    """
    Extract task description and date from query.
    """
    date_keywords = ["on", "by", "for", "before", "at"]  # Words that indicate a date
    words = query.split()

    for i, word in enumerate(words):
        if word.lower() in date_keywords and i < len(words) - 1:
            task = " ".join(words[:i])  # Task is everything before the keyword
            date = parse_date(" ".join(words[i + 1:]))  # Extract date
            return task.strip(), date
    
    return query.strip(), datetime.date.today().strftime("%Y-%m-%d")  # Default to today
def ToDOmain(query,first = False):
    """
    Handle all ToDo list queries.
    """
    query = query.lower().strip()

    if query.startswith("add reminder"):
        task, date = extract_task_and_date(query[12:])  # Extract task & date
        return add_task_db(task, date, True)

    elif query.startswith("add task"):
        task, date = extract_task_and_date(query[9:])  # Extract task & date
        return add_task_db(task, date, False)

    elif "show all my task" in query:
        start_Server()  # Start the Flask server if not already running
        open_todo_list() 
            # Open the task list UI, but DO NOT block execution
        return "All your task will be displayed in a while" 

    elif "show reminders" in query or "today's reminders" in query or "any reminders" in query or "reminders for today" in query or first:
        today = datetime.date.today().strftime("%Y-%m-%d") # Get today's date
        tasks = get_tasks_db()  # Fetch all tasks from DB

        reminders = [task["task"] for task in tasks if task.get("reminder") and task.get("date") == today]

        if reminders:
            return f"Here are your reminders for today:\n" + "\n".join(f"- {r}" for r in reminders)
        else:
            return "You have no reminders for today!"

    return False  # Function exits, but Flask keeps running



# Example Usage:
if __name__ == "__main__":
    print(ToDOmain("add reminder Buy groceries today"))
    print(ToDOmain("add task Finish project by 16th April"))
    print(ToDOmain("add task Call mom on 12-02-2025"))
    print(ToDOmain("add reminder Pay electricity bill by tomorrow"))
    print(ToDOmain("show tasks"))
