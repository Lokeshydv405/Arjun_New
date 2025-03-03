from groq import Groq
from config import apikey2

chatStr = ''  # Maintain chat history

def format_response(response):
    """
    Format the response for structured and clear output.
    - Detects and highlights code snippets.
    """
    formatted_response = []
    in_code_block = False
    code_detected = False

    for line in response.splitlines():
        if line.startswith("```"):  # Toggle code block
            in_code_block = not in_code_block
            code_detected = True
            formatted_response.append(line)
        elif in_code_block:
            formatted_response.append(line)
        else:
            formatted_response.append(f"* {line.strip()}")  # Add bullet points for text

    return "\n".join(formatted_response), code_detected


def chat(query):
    """
    Process user query through the Llama API and return a formatted response.
    """
    global chatStr
    query = query.strip()

    # Prepare the structured prompt
    newChat = f"Master: {query}\nArjun:"
    formatted_prompt = (
        f"You are Arjun, a helpful and intelligent desktop assistant. "
        f"Respond to the following query clearly and concisely:\n\n{query}\n\n"
        "You should respond briefly to various greetings, questions, and commands. "
        "You can use markdown formatting to make your responses more readable. "
        "Your response should be natural, friendly, and informative. "
        "only provide code if the user specifically asks for it.\n"
        "If the response includes code, wrap it in triple backticks (```python). "
        "First, provide all the code, then the explanation."
        "Do not answer anything that is not a chat question."
    )

    try:
        # Initialize the Groq client
        client = Groq(api_key=apikey2)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Collect response chunks
        text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                text += chunk.choices[0].delta.content

        # Clean and format response
        response_text = text.replace("Arjun:", "").strip()
        formatted_text, is_code = format_response(response_text)

        # Update chat history
        newChat += response_text + "\n"
        chatStr += newChat
        # remove all the * and other stuff
        formatted_text = formatted_text.replace("*", "")
        formatted_text = formatted_text.replace("_", "")
        
        return is_code, formatted_text  # Return flag and formatted response

    except Exception as e:
        print(f"Error: {e}")
        return False, "An error occurred. Please try again."


if __name__ == "__main__":
    # Test the function
    user_query = "Write a Python program to reverse a string."
    response = chat(user_query)
    print("\nFormatted Response:\n")
    print(response["response"])
