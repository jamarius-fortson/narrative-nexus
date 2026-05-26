import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def test_llm():
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com/v1",
        temperature=0.7
    )
    
    print("Sending test message to DeepSeek...")
    try:
        response = llm.invoke("Hi, please respond with only the word 'READY' if you are working.")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"LLM Error: {e}")

if __name__ == "__main__":
    test_llm()
