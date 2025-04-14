from openai import OpenAI
from dotenv import load_dotenv
from AI.contants import persona_system_prompt

load_dotenv();

client = OpenAI();

def invokeChat():
  query = input("> ")
  messages = [{
      "role": "system", "content": persona_system_prompt,
    },
    {
      "role": "user", "content": query
    }];
  response = client.chat.completions.create(model="gpt-4o", messages=messages)
  print(response.choices[0].message.content);