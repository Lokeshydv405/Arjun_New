import os
import re
from groq import Groq
from config import apikey2
from Basic_Utilities.say import say

# client = Groq(api_key=apikey2)  # Initialize globally
client = Groq(api_key="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")  # Initialize globally

def AI_Prompt_Writing(prompt):
    try:
        text = f'User Input : {prompt}\n' + "-" * 20 + "\n"
        prompt = prompt.replace("write", "")
        prompt = prompt.replace("arjun", "")
        
        formatted_prompt = (
        f"You are Arjun, a desktop assistant. Use the following request to generate a response:\n\n"
        f"\"{prompt}\"\n\n"
        "Provide a detailed, creative, and user-friendly output. Avoid technical jargon."
        )

        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
        text += response

        # Ensure the 'Answers' directory exists
        os.makedirs('Answers', exist_ok=True)

        # Sanitize and truncate the file name
        sanitized_prompt = re.sub(r'[\\/*?:"<>|]', '_', prompt.split('write')[-1].strip()[:20]) or "response"
        file_name = os.path.join('Answers', f'{sanitized_prompt}.txt')

        # Write the response to the file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(text)

        print("Done, check for the file in the Answers folder.")
        say("Done, check for the file in the Answers folder.")
        return response

    except Exception as e:
        print(f"Error: {e}")
        # say("An error occurred. Please check the logs.")
        return False
if __name__ == "__main__":
    prompt = "Write a story about a dragon and a knight."
    AI_Prompt_Writing(prompt)
    prompt = "Write a poem about the ocean."
    AI_Prompt_Writing(prompt)
    prompt = "Write a story about a Lion and mouse"
    AI_Prompt_Writing(prompt)
    prompt = "Write a poem about the stars."
    AI_Prompt_Writing(prompt)
    prompt = "Write a story about a haunted house."
    
