from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def ask_chatbot(question: str) -> str:
    if not question.strip():
        return "Please enter a valid question."

    prompt = f"""
You are an e-commerce customer support assistant.
Answer clearly and step-by-step.

Question:
{question}
"""

    result = generator(
        prompt,
        max_length=200,
        do_sample=False
    )

    return result[0]["generated_text"]
