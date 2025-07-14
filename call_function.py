from google.genai import types

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    function_args["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        try:
            function_to_call = functions[function_name]
            function_result = function_to_call(**function_args)

            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )
        except Exception as e:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=e,
                        response={"error": f"{e.response}"},
                    )
                ],
            )
            
    