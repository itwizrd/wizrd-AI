import os
import subprocess
def run_python_file(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        subprocess.run(["python3", f"{abs_file_path}"], stdout=print(f"STDOUT:{subprocess.PIPE}"), stderr=print(f"STDERR:{subprocess.PIPE}"), timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"