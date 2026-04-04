import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate(message):
    client = genai.Client()

    chat = client.chats.create(
        model="gemini-3.1-pro-preview",
        config=types.GenerateContentConfig(
            max_output_tokens=8192,
            top_k=40,
            top_p=0.95,
            temperature=1.0, 
                       
        ),
    )
    
    try:
            response = chat.send_message(message)
            return (response.text)
    except Exception as e:
           print(f"GEMINI ERROR: {str(e)}, {response.status_code} - {response.text}") 
           return("this service is currently unavailable")

if __name__ == "__main__":

    print(generate())