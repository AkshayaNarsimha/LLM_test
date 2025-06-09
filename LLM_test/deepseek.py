import os
from openai import OpenAI

# ✅ Replace with your OpenRouter API Key
OPENROUTER_API_KEY = "your_api_key"

# ✅ Initialize OpenAI for OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ✅ Load your prompt template from file
def load_prompt():
    with open("prompt_template.txt", "r", encoding="utf-8") as f:
        return f.read()

# ✅ Read original test file content
def load_test_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ✅ Save the generated output
def save_output(output_path, content):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

# ✅ Transform one file using the specified model
def transform_file(model_id, input_path, output_path):
    prompt = load_prompt()
    test_code = load_test_file(input_path)
    full_prompt = prompt + "\n\n```python\n" + test_code + "\n```"

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a Python readability expert."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.4
        )
        generated = response.choices[0].message.content
        save_output(output_path, generated)
        print(f"✅ Transformed: {input_path} → {output_path}")
    except Exception as e:
        print(f"❌ Error transforming {input_path}: {e}")

# ✅ Process all test files in /data and save to output directory
def run_all(model_id="deepseek/deepseek-chat:free", output_dir="deepseek_outputs"):
    input_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".py"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            transform_file(model_id, input_path, output_path)

if __name__ == "__main__":
    # Example: switch to Gemma with a single change
    run_all(model_id="google/gemma-3-1b-it:free", output_dir="gemma_outputs")
