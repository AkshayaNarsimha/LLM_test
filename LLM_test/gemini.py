import os
from openai import OpenAI
import time

# ✅ Replace with your OpenRouter API Key
OPENROUTER_API_KEY = "your_api_key"

# ✅ Initialize OpenAI (OpenRouter) Client
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ✅ Load your prompt template
def load_prompt():
    with open("prompt_template.txt", "r", encoding="utf-8") as f:
        return f.read()

# ✅ Read a test file
def load_test_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ✅ Save the transformed code
def save_output(output_path, content):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

# ✅ Use Gemini to transform a Python test file
def transform_with_gemini(input_path, output_path):
    prompt = load_prompt()
    test_code = load_test_file(input_path)
    full_prompt = prompt + "\n\n```python\n" + test_code + "\n```"

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {"role": "system", "content": "You are a Python readability expert."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3
        )
        generated = response.choices[0].message.content
        save_output(output_path, generated)
        print(f"✅ Transformed: {input_path} → {output_path}")
    except Exception as e:
        print(f"❌ Error transforming {input_path}: {e}")

# ✅ Transform all .py test files in /data to /gemini_outputs
def run_all():
    input_dir = "data"
    output_dir = "gemini_outputs"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".py"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            transform_with_gemini(input_path, output_path)
            time.sleep(60)  # ⏳ Wait 20 seconds to avoid rate limit

if __name__ == "__main__":
    run_all()
    
