import ollama

# Initial chat with Ollama to explain Newton's second law of motion
response = ollama.chat(
    model="deepseek-r1:1.5b",
    messages=[
        {"role": "user", "content": "Describe Chinese Spring Festival in simple words"},
    ],
)
print(response["message"]["content"])
