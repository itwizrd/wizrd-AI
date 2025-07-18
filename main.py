import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import *
from config import MAX_ITERATION

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    
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
    verbose = "--verbose" in sys.argv
    if verbose:
        print(f"""
            User prompt: {user_prompt}
            """)
    
    count = 0
    while True:
        count += 1
        if count > MAX_ITERATION:
            print(f"Maximum Iterations reached: {MAX_ITERATION}\n cannot continue")
            sys.exit(1)
        try:
            is_done, final_response, messages = generate_content(client, messages, verbose)
            if is_done:
                print(f"Final Response:\n{final_response}")
                break
        except Exception as e:
            print(f"Error in generated_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    for candidate in response.candidates:
        messages.append(candidate.content)
    if verbose:
        print(f"""
            Prompt tokens: {response.usage_metadata.prompt_token_count}
            Response tokens: {response.usage_metadata.candidates_token_count}
            """)
    if not response.function_calls:
        return True, response.text, messages
    for f in response.function_calls:
        try:
            function_call_result = call_function(f, verbose)
            if not function_call_result.parts or len(function_call_result.parts) == 0:
                raise Exception("No output from function")
            # loop each response as a tool response so the prompt can follow conversation
            messages.append(types.Content(
                role="tool",
                parts=[function_call_result.parts[0]]
            ))
        except Exception as e:
            raise Exception(f"Fatal exception, please check your inputs: tool call error: {e}")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    return False, None, messages


if __name__ == "__main__":
    main()