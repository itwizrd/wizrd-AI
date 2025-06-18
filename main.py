
import os
from dotenv import load_dotenv


from google import genai
from google.genai import types


import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI code assistant")
        sys.exit(1)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = generate_content(client,messages)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")

def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    return response
    

if __name__ == "__main__":
    main()