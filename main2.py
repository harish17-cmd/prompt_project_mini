import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

conversation = []

MAX_MESSAGES = 4

print("Context Window Demo")
print("Type 'exit' to stop.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    conversation.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Keep only the latest messages
    conversation = conversation[-MAX_MESSAGES:]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation,
        temperature=0.3
    )

    answer = response.choices[0].message.content

    print("\nAI:", answer)

    conversation.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    conversation = conversation[-MAX_MESSAGES:]
