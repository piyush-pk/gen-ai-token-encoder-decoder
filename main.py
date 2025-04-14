from gemini_chat import cot as gemini_cot, persona as gemini_persona
from openai_chat import cot as open_ai_cot, persona as open_ai_persona, agent

def main():
    # open_ai_cot.invokeChat();
    # open_ai_persona.invokeChat();
    
    # gemini_cot.invokeChat();
    # gemini_persona.invokeChat();

    agent.invokeChat();
    
if __name__ == "__main__":
    main()
