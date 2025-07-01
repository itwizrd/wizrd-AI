import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from functions.get_files_info import *

def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    return response

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("""
              Welcome to Wizrd AI, your gemini based code assistant
              Usage: python main.py "your prompt here" [--verbose]
              Example: python main.py "How do I build a calculator app?"
              """)
        sys.exit(1)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = generate_content(client,messages)
    if verbose:
        print(f"""
            User prompt: {user_prompt}
            Prompt tokens: {response.usage_metadata.prompt_token_count}
            Response tokens: {response.usage_metadata.candidates_token_count}
            """)
    if response.function_calls:
        for f in response.function_calls:
            print(f"Calling function: {f.name}({f.args})")
    else:
        print(f"Response:{response.text}")

if __name__ == "__main__":
    main()