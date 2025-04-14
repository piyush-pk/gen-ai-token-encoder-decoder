from openai import OpenAI
from dotenv import load_dotenv
from AI.contants import cot_system_prompt
import json

load_dotenv();

client = OpenAI();

def invokeChat():
  query = input("> ")
  messages = [{
      "role": "system", "content": cot_system_prompt,
    },
    {
      "role": "user", "content": query
    }];
  while True:
    response = client.chat.completions.create(model="gpt-4o", response_format={"type": "json_object"}, messages=messages)
    print('\n\n' + json.loads(response.choices[0].message.content)['step'] + ": " + json.loads(response.choices[0].message.content)['content'] + '\n\n');

    if json.loads(response.choices[0].message.content)['step'] == 'result':
      break;

    messages.append({"role": "assistant", "content": json.dumps(response.choices[0].message.content)});