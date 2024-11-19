import os
import google.generativeai as genai

genai.configure(api_key="") 

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 512, 
    "response_mime_type": "text/plain",
}

def generate_function_code(name, params, prompt, return_type):
    param_str = ', '.join(params)
    
    function_prompt = f"Generate only the Java function '{name}' with parameters ({param_str}) that {prompt}. " \
                      f"The function should be static with a return type of {return_type}. " \
                      "Only output the function signature and body without any additional text or explanations. Dont output their fuction name or parameters, only the body. If it says to print print them otherwise dont."

    try:

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        chat_session = model.start_chat(history=[])

        response = chat_session.send_message(function_prompt)
        generated_code = response.text.strip()

        generated_code = generated_code.replace("```java", "").replace("```", "").strip()

        if "public static" not in generated_code:
            generated_code = f"public static {return_type} {name}({param_str}) {{\n{generated_code}\n}}"

        if not generated_code.strip().endswith("}"):
            generated_code += "\n}"

        return generated_code + "\n"
    
    except Exception as e:
        print("Error generating function:", e)
        return f"// Error generating function {name}\n"
