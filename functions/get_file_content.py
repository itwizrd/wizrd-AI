import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads out the first 10k char of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    is_file = os.path.isfile(abs_file_path)
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not is_file:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        max_char = 10000
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(max_char)
            if f.read(1):
                return f'{file_content_string}[...File "{file_path}" truncated at {max_char} characters]'
            else:
                return file_content_string
    except Exception as e:
        return f"Error: {e}"