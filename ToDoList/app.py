from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os
import signal
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["arjun_assistant"]
tasks_collection = db["tasks"]

def add_task_db(task, date, is_reminder):
    """Function to add a task directly to the database"""
    task_data = {"task": task, "date": date, "completed": False, "reminder": is_reminder}
    tasks_collection.insert_one(task_data)
    return "Task added successfully!"

def get_tasks_db():
    """Function to fetch all tasks"""
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    tasks.sort(key=lambda x: x.get("date", ""))
    return tasks

def update_task_db(task_name):
    """Function to toggle task completion"""
    task = tasks_collection.find_one({"task": task_name})
    if task:
        new_status = not task.get("completed", False)  # Toggle status
        tasks_collection.update_one({"task": task_name}, {"$set": {"completed": new_status}})
        return "Task status updated!"
    return "Task not found!"

def delete_task_db(task_name):
    """Function to delete a task"""
    tasks_collection.delete_one({"task": task_name})
    return "Task deleted successfully!"

@app.route("/")
def home():
    return render_template("list_frontend.html")

@app.route("/add_task", methods=["POST"])
def add_task():
    """Flask route to add a task"""
    data = request.json
    task = data.get("task")
    date = data.get("date")  
    is_reminder = data.get("reminder", False)
    return jsonify({"message": add_task_db(task, date, is_reminder)}), 201

@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    """Flask route to get all tasks"""
    return jsonify(get_tasks_db())

@app.route("/update_task", methods=["POST"])
def update_task():
    """Flask route to toggle task completion"""
    data = request.json
    task_name = data.get("task")
    return jsonify({"message": update_task_db(task_name)})

@app.route("/delete_task", methods=["POST"])
def delete_task():
    """Flask route to delete a task"""
    data = request.json
    task_name = data.get("task")
    return jsonify({"message": delete_task_db(task_name)})

@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Shut down the Flask server from the frontend"""
    os.kill(os.getpid(), signal.SIGTERM)  # Kills the process
    return jsonify({"message": "Server shutting down..."})

if __name__ == "__main__":
    app.run(debug=True)
