import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to file, creating the necessary directories and overwritting any current content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write, relative to the working directory, creating any subdirectories as needed.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write to the specified path."
            ),
        },
        required=["file_path", "content"],
    ),
)
def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    try:
        with open(abs_file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    