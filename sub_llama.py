
#pip install ollama
#sudo snap install ollama

#ollama run llama3
import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Tell me an interesting fact about elephants",
        },
    ],
)
print(response["message"]["content"])
print("Complete")