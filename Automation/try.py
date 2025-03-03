# Open the file in write mode ('w'). This will create the file if it doesn't exist.
# If the file already exists, it will overwrite its contents.
with open("example.txt", "w") as file:
    file.write("Hello, this is a simple text written to the file!")
