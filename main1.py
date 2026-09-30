import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

conversation = [
    {
        "role": "system",
        "content": (
            "You are a friendly AI assistant. "
            "Answer clearly and remember the conversation."
        )
    }
]

print("AI Chatbot")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    conversation.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation,
        temperature=0.3
    )

    assistant_reply = response.choices[0].message.content

    print(f"\nAI: {assistant_reply}\n")

    conversation.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )