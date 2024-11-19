import os
import sys
from parser import parse_file
from compiler import compile_java
import subprocess

def main(file_path):
    output_file = parse_file(file_path)
    
    if output_file is None:
        print("Error: Parsing failed.")
        return

    try:
        compile_java(output_file)
    except Exception as e:
        print("Compilation error.")
        return

    class_name = os.path.splitext(os.path.basename(output_file))[0]
    run_command = ["java", "-cp", "output", class_name]
    
    result = subprocess.run(run_command, capture_output=True, text=True)
 
    print(result.stdout.strip())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if os.path.isfile(file_path):
        main(file_path)
    else:
        print("Error: File not found.")
