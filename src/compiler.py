import subprocess
import os

def compile_java(file_path):
    compile_command = f"javac {file_path}"
    try:
        subprocess.run(compile_command, shell=True, check=True)
        print(f"Compilation successful\n")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")
