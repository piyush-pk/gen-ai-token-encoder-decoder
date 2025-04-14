import google.generativeai as genai
from dotenv import load_dotenv;
import os
import json
import sys

# ✅ Add project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Now import works
from AI.contants import persona_system_prompt

load_dotenv();
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash", 
  system_instruction=persona_system_prompt, 
  # generation_config={ "response_mime_type": "application/json" }
  ).start_chat();

def invokeChat():
  query = input("> ");
  response = model.send_message(query);
  print(response.text)