import os
from openai import OpenAI

# ✅ Your OpenRouter API key here
OPENROUTER_API_KEY = "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"  # Replace with your key


# ✅ Initialize OpenAI for OpenRouter with Llama 3.2 1B
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ✅ Load prompt template from file
def load_prompt():
    with open("prompt_template.txt", "r", encoding="utf-8") as f:
        return f.read()

# ✅ Load a single test file
def load_test_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ✅ Save the generated transformation
def save_output(output_path, content):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

# ✅ Perform transformation using Llama 3.2 1B
def transform_with_llama_1b(input_path, output_path):
    prompt_template = load_prompt()
    original_code = load_test_file(input_path)
    full_prompt = prompt_template + "\n\n```python\n" + original_code + "\n```"

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-1b-instruct:free",
            messages=[
                {"role": "system", "content": "You are a Python code readability and quality expert."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.4,
            max_tokens=1024
        )
        generated = response.choices[0].message.content
        save_output(output_path, generated)
        print(f"✅ Transformed: {input_path} → {output_path}")
    except Exception as e:
        print(f"❌ Error transforming {input_path}: {e}")

# ✅ Process all files in input folder
def run_all():
    input_dir = "data"
    output_dir = "llama_outputs"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".py"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            transform_with_llama_1b(input_path, output_path)

if __name__ == "__main__":
    run_all()
