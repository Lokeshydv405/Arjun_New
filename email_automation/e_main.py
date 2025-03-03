from simplegmail import Gmail
from simplegmail.query import construct_query

# Authenticate and create a Gmail instance
gmail = Gmail()

# Define allowed senders (ensure they match the format in fetched emails)
allowed_senders = ["acadoffice@iitmandi.ac.in", "krishna@iitmandi.ac.in","edc@students.iitmandi.ac.in","placement@iitmandi.ac.in","technical_secretary@students.iitmandi.ac.in","deanstudentsoffice@iitmandi.ac.in",]

# Set query to get emails from specific senders
query_params = {
    "newer_than": (1, "day"),
}

# Fetch received messages
messages = gmail.get_messages(query=construct_query(query_params))

# List to store emails
email_list = []

# Process each message
for message in messages:
    sender_email = message.sender.split("<")[-1].strip(">").lower()  # Extract only the email ID
    print(sender_email)
    if sender_email in allowed_senders:  # Check against allowed senders
        email_data = {
            "id": message.id,
            "date": message.date,
            "sender": message.sender,
            "email_id": sender_email,
            "subject": message.subject,
            "body": message.plain if message.plain and len(message.plain) < 1000 else "Body too long or unavailable"
        }

        email_list.append(email_data)

# Print the email list
print(email_list)


