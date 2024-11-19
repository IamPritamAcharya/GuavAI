import re
import os
from ai_function_gen import generate_function_code

def parse_file(file_path):
    """
    Reads a .guav file, translates its syntax to Java, and writes the output Java code to a file.
    Returns the path of the generated Java file.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

    java_code = ["import java.util.*;\n\n"]  # Add import statement at the top
    output_filename = None

    for line in lines:
        line = line.strip()  # Remove any leading/trailing whitespace

        # Parse output filename
        if line.startswith("@"):
            output_filename = parse_output_filename(line)
            if output_filename:
                java_code.append(f"public class {output_filename.replace('.java', '')} {{\n")
        
        # Translate function syntax
        elif line.startswith("func "):
            function_declaration = translate_function_syntax(line)
            if function_declaration:
                java_code.append(function_declaration + " {\n")
                # If this is the main function, insert Scanner instantiation
                if "public static void main(String[] args)" in function_declaration:
                    java_code.append("    Scanner sc = new Scanner(System.in);\n")
        
        # Parse AI function (using ### marker)
        elif line.startswith("###"):
            func_code = parse_ai_function(line)
            if func_code:
                java_code.append(func_code)
        
        # Translate regular syntax and control structures
        else:
            translated_line = translate_syntax(line)
            if translated_line:
                # Add a semicolon only if it is not a control structure or a brace
                if not (translated_line.endswith("{") or translated_line.endswith("}")):
                    translated_line = translated_line.rstrip(";")  # Remove any existing semicolon
                    translated_line += ";"
                java_code.append(translated_line + "\n")

    # Ensure output filename is set
    if not output_filename:
        print("Error: Output filename not defined in the .guav file.")
        return None

    # Close the class definition properly
    java_code.append("}\n")

    # Write the generated Java code to output file
    output_path = f"output/{output_filename}"
    os.makedirs("output", exist_ok=True)
    
    with open(output_path, 'w') as output_file:
        output_file.writelines(java_code)
    
    return output_path

# Helper functions unchanged.


def parse_output_filename(line):
    """
    Parses the filename from a line that starts with '@' and returns the Java filename.
    """
    return line[1:].strip() + ".java"

def translate_function_syntax(line):
    """
    Translates guavAI function syntax to Java.
    Default values: scope = 'public', static = 'static', return type = 'void'
    """
    # Update the regex to support all common Java types and array types
    match = re.match(
        r"func\s*(public|protected|private)?\s*(static|nonstatic)?\s*"
        r"(void|int|double|String|char|boolean|float|long|short|byte"
        r"|int\[\]|double\[\]|String\[\]|char\[\]|boolean\[\]|float\[\]|long\[\]|short\[\]|byte\[\])?\s+"
        r"(\w+)\((.*)\)", 
        line
    )
    
    if match:
        # Apply default values if components are missing
        scope = match.group(1) or "public"
        is_static = "static" if not match.group(2) or match.group(2) == "static" else ""
        return_type = match.group(3) or "void"
        function_name = match.group(4)
        parameters = match.group(5)
        
        # Construct Java syntax ensuring spacing is correct
        static_part = f"{is_static} " if is_static else ""
        return f"{scope} {static_part}{return_type} {function_name}({parameters})"
    else:
        print(f"Warning: Function syntax invalid in line: {line}")
    return ""


def parse_ai_function(line):
    """
    Parses a line that specifies an AI-generated function with syntax:
    ###<function_name>(<parameters>) # <prompt> #<return_type>
    Calls the AI to generate function code based on the provided prompt.
    """
    # Updated regex to capture function name, parameters, prompt, and return type
    match = re.match(r"###\s*(\w+)\s*\(\s*(.*)\s*\)\s*#\s*(.+)\s*#\s*(\w+)", line)


    
    if match:
        func_name = match.group(1)
        params = [param.strip() for param in match.group(2).split(",") if param]
        prompt = match.group(3)
        return_type = match.group(4)
        
        # Call generate_function_code from ai_function_generator.py
        generated_code = generate_function_code(func_name, params, prompt, return_type)
        return generated_code
    else:
        print(f"Warning: AI function syntax invalid in line: {line}")
    return ""


def translate_syntax(line):
    """
    Translates custom .guav syntax to Java code, including handling variable declarations
    with input.<Type>() or <variable> = next<Type>() syntax using the Scanner instance.
    """
    syntax_mappings = {
        "shout": "System.out.println",     # Default print with newline
        "output": "System.out.print",     # Print without newline
        "main()": "public static void main(String[] args)"
    }

    # Control structure translations
    if line.startswith("loop("):
        return line.replace("loop(", "for(").rstrip(")")  # Replace `loop` with `for`
    elif line.startswith("foreach("):
        return line.replace("foreach(", "for(").rstrip(")")
    elif line.startswith("until("):
        return line.replace("until(", "while(").rstrip(")")
    
    # Apply syntax mappings
    for key, java_equivalent in syntax_mappings.items():
        line = line.replace(key, java_equivalent)

    # Match both input.<Type>() and next<Type>() syntax
    input_match = re.match(r"(\w+)\s+(\w+)\s*=\s*input\.(\w+)\s*\(\);", line)
    next_match = re.match(r"(\w+)\s+(\w+)\s*=\s*next(\w+)\s*\(\);", line)

    if input_match:
        var_type = input_match.group(1)
        var_name = input_match.group(2)
        input_type = input_match.group(3)
        scanner_method = f"sc.next{input_type.capitalize()}()"
        return f"{var_type} {var_name} = {scanner_method};"
    elif next_match:
        var_type = next_match.group(1)
        var_name = next_match.group(2)
        next_type = next_match.group(3)
        scanner_method = f"sc.next{next_type.capitalize()}()"
        return f"{var_type} {var_name} = {scanner_method};"

    # Handle main method instantiation with Scanner declaration
    if "public static void main(String[] args)" in line:
        line += "\n    Scanner sc = new Scanner(System.in);"

    # Match and translate array declarations with inline values using curly braces
    inline_array_declaration_match = re.match(r"arr\((\w+)\)\s+(\w+)\s*=\s*\{(.*)\};", line)
    if inline_array_declaration_match:
        data_type = inline_array_declaration_match.group(1)
        variable = inline_array_declaration_match.group(2)
        values = inline_array_declaration_match.group(3)
        return f"{data_type}[] {variable} = {{{values}}};"

    # Match and translate array assignments from function calls
    function_array_assign_match = re.match(r"arr\((\w+)\)\s+(\w+)\s*=\s*([\w\.]+)\((.*)\);", line)
    if function_array_assign_match:
        data_type = function_array_assign_match.group(1)
        variable = function_array_assign_match.group(2)
        function_call = function_array_assign_match.group(3)
        parameters = function_array_assign_match.group(4)
        return f"{data_type}[] {variable} = {function_call}({parameters});"

    # Match and translate array declarations with a specified size
    size_array_declaration_match = re.match(r"arr\((\w+)\)\s+(\w+)\s*=\s*size\((\d+)\);", line)
    if size_array_declaration_match:
        data_type = size_array_declaration_match.group(1)
        variable = size_array_declaration_match.group(2)
        size = size_array_declaration_match.group(3)
        return f"{data_type}[] {variable} = new {data_type}[{size}];"

    # Remove redundant semicolons and misplaced braces
    line = re.sub(r';{2,}', ';', line)  # Remove multiple semicolons
    line = re.sub(r'{\s*{', '{', line).replace('} }', '}')  # Fix misplaced braces

    return line if line else None


def translate_array_syntax(line):
    """
    Translates guavAI array declaration to Java syntax.
    """
    # Array initialization with elements, e.g., arr(int) arr = {1, 2, 3};
    init_match = re.match(r"arr\((\w+)\)\s+(\w+)\s*=\s*\{(.+?)\};", line)
    if init_match:
        data_type = init_match.group(1)
        variable = init_match.group(2)
        elements = init_match.group(3)
        return f"{data_type}[] {variable} = {{{elements}}};"
    
    # Array declaration with size, e.g., arr(int) arr = size(5);
    size_match = re.match(r"arr\((\w+)\)\s+(\w+)\s*=\s*size\((\d+)\);", line)
    if size_match:
        data_type = size_match.group(1)
        variable = size_match.group(2)
        size = size_match.group(3)
        return f"{data_type}[] {variable} = new {data_type}[{size}];"
    
    print(f"Warning: Array syntax invalid in line: {line}")
    return ""
