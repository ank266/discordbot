import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

ai_chat_history_file_location = "data_storage/ai_chat_history.txt"

def gemini_AI_Response(text):
    fullContext = read_AI_Chat_History()
    response = model.generate_content(fullContext + text)
    append_AI_Chat_History("User", text)
    append_AI_Chat_History("Gemini Bot", response.text)
    return response.text

def append_AI_Chat_History(speaker, text):
    f = open(ai_chat_history_file_location, "a")
    f.write(speaker + ": " + text+"\n")
    f.close()

def clear_AI_Chat_History():
    with open(ai_chat_history_file_location, 'w') as file:
        pass

def read_AI_Chat_History():
    check_If_AI_History_File_Exists()
    f = open(ai_chat_history_file_location, "r")
    return f.read()

def check_If_AI_History_File_Exists():
    if not os.path.exists(ai_chat_history_file_location):
        with open(ai_chat_history_file_location, 'w') as file:
            pass
