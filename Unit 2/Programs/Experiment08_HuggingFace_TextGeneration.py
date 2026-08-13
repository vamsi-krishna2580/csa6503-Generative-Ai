from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_API_KEY")
)

prompt = input("Enter Prompt: ")

response = client.chat_completion(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\nGenerated Text:\n")
print(response.choices[0].message.content)