import google.generativeai as genai
from dotenv import load_dotenv
import json
import requests
import subprocess
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the model (e.g., gemini-1.5-pro or gemini-1.5-flash)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Weather API function
def get_weather(city: str):
    result = requests.get(f"https://wttr.in/{city}?format=3")
    if result.status_code != 200:
        return 'something went wrong !!!'
    return result.text

# Command execution function
def run_command(command: str):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
    except Exception as e:
        return str(e)

# Available tools
available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "takes a input as city name and return weather of the city."
    },
    "run_command": {
        "fn": run_command,
        "description": "takes a input as command and run it into the system e.g. create files list files or network check all kind of commands. all kind of os access can be done using this tool by providing commands"
    },
}

available_tools_str = {key: value['description'] for key, value in available_tools.items()}

# System prompt (same as original)
system_prompt = f"""
    you're a smart and helpful AI assistant who specializes in solving problems and resolving user queries.
    You work in start, understand, plan, action, observe mode.
    For the given user's query and available tools, plan the step-by-step execution. Based on the plan, if an external tool is required, select the relevant tool from the available tools.
    Based on the tool selection, perform an action to call the tool, wait for the observation, and resolve the user query based on the observation.

    Rules:
    1. Always perform one step at a time.
    2. Always return JSON response.
    3. Carefully analyze the query and call a tool only when required.
    4. If an error occurs while running the tool, understand the error, validate the input, and retry if necessary.

    Output JSON Format:
    {{ 
      "step": "string", 
      "content": "string", 
      "function": "function name if step is action.",
      "input": "the input parameter for the function"
    }}

    Available Tools:
    {json.dumps(available_tools_str)}
    
    Example:
    user query: what is the weather of nashik ?
    output: {{ "step": "understand", "content": "user is interested in weather data of nashik." }}
    output: {{ "step": "plan", "content": "from the available tools I should call get_weather for getting complete info of Nashik weather." }}
    output: {{ "step": "action", "function": "get_weather", "input": "Nashik" }}
    output: {{ "step": "observe", "content": "12 degree cel." }}
    output: {{ "step": "output", "content": "the weather of Nashik is 12 degree cel, you should have your partner nearby with a hot coffee." }}
"""

def invokeChat():
    # Get user query
    query = input("> ")
    
    # Initialize message history
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    while True:
        # Prepare the prompt by combining messages
        prompt = "\n".join([msg["content"] for msg in messages])
        
        # Call Gemini API
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",  # Enforce JSON output
                    "temperature": 0.3,  # Lower temperature for structured output
                }
            )
            
            # Extract and parse the response
            data = json.loads(response.text)  # Gemini returns JSON string in text
            print('\n\n\n', data)

            # Add response to message history
            messages.append({"role": "assistant", "content": json.dumps(data)})

            # Check if the step is 'output' to break the loop
            if data['step'] == 'output':
                print(data['content'])
                break

            # Handle 'action' step
            if data['step'] == 'action':
                fn = data.get('function')
                arg = data.get('input')

                if fn in available_tools:
                    result = available_tools[fn]['fn'](arg)
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({"step": "observe", "content": result})
                    })
                else:
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({
                            "step": "error",
                            "content": f"Tool {fn} not found."
                        })
                    })

        except Exception as e:
            # Handle errors (e.g., invalid JSON, API errors)
            error_data = {
                "step": "error",
                "content": f"Error processing response: {str(e)}"
            }
            print(error_data)
            messages.append({"role": "assistant", "content": json.dumps(error_data)})
            break