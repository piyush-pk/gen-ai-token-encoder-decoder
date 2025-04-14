import google.generativeai as genai
from dotenv import load_dotenv;
import os
import json
import sys

# ✅ Add project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Now import works
from AI.contants import cot_system_prompt

load_dotenv();
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-2.0-flash", system_instruction=cot_system_prompt,  generation_config={ "response_mime_type": "application/json" }).start_chat();

def invokeChat():
  query = input("> ");
  response = model.send_message(query);
  print(f"\n\n {json.loads(response.text)['step']}: {json.loads(response.text)['content']}")

  while True:
    if json.loads(response.text)['step'] != 'result':
      response = model.send_message('next step')
      print(f"\n\n\n {json.loads(response.text)['step']}: {json.loads(response.text)['content']}")
      continue;

    break;