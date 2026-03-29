import os
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def format_transactions(transactions: List[Dict[str, Any]]) -> str:
    if not transactions:
        return "No transactions found."

    lines = []
    for t in transactions:
        line = (
            f"- Date: {t['transactionDate']} | "
            f"Type: {t['type']} | "
            f"Category: {t['category']} | "
            f"Amount: ₹{t['amount']} | "
            f"Description: {t['description']}"
        )
        lines.append(line)

    return "\n".join(lines)


def build_chain():
    llm = OllamaLLM(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL
    )

    prompt = PromptTemplate(
        input_variables=["transactions", "question"],
        template="""You are a personal finance assistant. 
You have access to the user's transaction history below.
Answer the user's question based only on this data.
Be concise, specific, and helpful.

Transaction History:
{transactions}

User Question: {question}

Answer:"""
    )

    return prompt | llm | StrOutputParser()


async def get_insight(transactions: List[Dict[str, Any]], question: str) -> str:
    context = format_transactions(transactions)
    chain = build_chain()
    return chain.invoke({
        "transactions": context,
        "question": question
    })