from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key="YOUR_HF_API_KEY"
)

prompt = input("Enter Prompt: ")

response = client.text_generation(
    prompt,
    model="mistralai/Mistral-7B-Instruct-v0.3"
)

print(response)
