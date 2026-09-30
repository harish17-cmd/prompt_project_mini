import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

context = """
Python is a high-level programming language.

It was created by Guido van Rossum.

The first public release was in 1991.
"""

question = input("Ask a question about Python: ")

prompt = f"""
You are a factual assistant.

Use ONLY the information provided below.

Context:
{context}

Question:
{question}

Rules:
- If the answer is present in the context, answer it.
- If the answer is NOT present, reply exactly:
"I don't have enough information to answer that from the provided context."
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)

print("\nContext")
print("-" * 50)
print(context)

print("\nAI Response")
print("-" * 50)
print(response.choices[0].message.content)
