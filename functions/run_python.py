import os
import subprocess
def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        run = subprocess.run(
            ["python3", f"{abs_file_path}"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )
        output = []
        if run.stdout:
            output.append(f"STDOUT:\n{run.stdout}")
        if run.stderr:
            output.append(f"STDERR:\n{run.stderr}")
        if run.returncode != 0:
            output.append(f"Process exited with code {run.returncode}")
        if output:
            return "\n".join(output)
        else:
            return "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"