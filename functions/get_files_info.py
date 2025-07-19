import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
def get_files_info(working_directory, directory=None):
    if working_directory is None:
        raise ValueError("working_directory is missing in get_files_info")
    abs_dir = os.path.abspath(os.path.join(working_directory, directory or ""))
    is_dir = os.path.isdir(abs_dir)
    
    # returning strings as errors so the LLM can read the error and try a different approach
    if not is_dir:
        return f'Error: "{directory}" is not a directory'
    if not abs_dir.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    try:
        dir_contents = []
        for i in os.listdir(abs_dir):
            file = os.path.join(abs_dir, i)
            file_size = os.path.getsize(file)
            file_dir = os.path.isdir(file)
            dir_contents.append(
                f"- {i}, file_size={file_size} bytes, is_dir={file_dir}\n"
            )
        return "\n".join(dir_contents)
    except Exception as e:
        return f"Error listing files: {e}"
