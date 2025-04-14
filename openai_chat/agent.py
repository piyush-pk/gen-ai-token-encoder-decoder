from openai import OpenAI
from dotenv import load_dotenv
import json;
import requests;
import subprocess

load_dotenv();

client = OpenAI();

def get_weather(city: str):
  result = requests.get(f"https://wttr.in/{city}?format=3");

  if result.status_code != 200:
    return 'something went wrong !!!';

  return result.text;

def run_command(command: str):
  try:
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    return result.stdout;
  except subprocess.CalledProcessError as e:
    return e.stderr  # Return stderr from the exception object
  except Exception as e:
    return e;



available_tools = {
  "get_weather": {
    "fn": get_weather,
    "description": "takes a input as city name and return weather of the city."
  },
  "run_command": {
    "fn": run_command,
    "description": "takes a input as command and run it into the system e.g. create files list files or network check all kind of commands."
  },
}

available_tools_str = { key: value['description'] for key, value in available_tools.items() }

sytem_prompt = f"""
    you're a smart and help ai assistant who is specialized to helping in every problem, and resolve the user query.
    You word on start, understand, plan, action, observe mode.
    for the given users query and available tools, plan the step by step execution, based on the planning, if any external tool required, select the relevent tool from the available tools.
    and based on the tool selection perform an action to call the tool, wait for the observation and based on observation from the tool call the resolve the user query.

    Rules:
    1. Always perform one step at a time.
    2. always return json response
    3. carefully analyse the query carefully, and call tool when it's required.
    4. if any error came in while running the tool understand the error again call in correct way may be input is wrong or something validate input before giving to the tool.

    Output Json Format:
    {{ 
      "step": "string", 
      "content": "string", 
      "function": "function name if step is action.",
      "input": "the input parameter for the function"
    }}

    Available Tools:
    { available_tools_str }
    
    Example:
    user query: what is the weather of nashik ?
    output: {{ "step": "understand", "content": "user is intersted in weather data of nashik." }}
    output: {{ "step": "plan", "content": "from the available tools i should call get_weather for getting complete info of nashik weather." }}
    output: {{ "step": "action", "function": "get_weather", "input": "Nashik" }}
    output: {{ "step": "observe", "content": "12 degree cel." }}
    output: {{ "step": "output", "content": "the weather of Nashik is seems 12 degree cel, you should have your partner nearby with a hot coffee." }}

"""

def invokeChat():

  query = input("> ");
  run_command(query);
  messages = [
    {
      "role": "system", "content": sytem_prompt
    },
    {
      "role": "user", "content": query
    }
  ];


  while True:
    response = client.chat.completions.create(model="gpt-4o", response_format={"type": "json_object"}, messages=messages);

    data = json.loads(response.choices[0].message.content);

    print(data)

    if data['step'] != 'output':
      messages.append({ "role": "assistant", "content": json.dumps(data)});

      if data['step'] == 'action':
        fn = data['function'];
        arg = data['input'];

        if available_tools.get(fn, False) != False:
          result = available_tools[fn]['fn'](arg);
          messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe",  "content": result }) });
          continue;

      continue;

    print(data['content']);

    break;

