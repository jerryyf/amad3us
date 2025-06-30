from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate

def rag_prompt(query: str, context: str) -> list[BaseMessage]:
    prompt = PromptTemplate.from_template("""
        You are an expert in psychoanalysis. Use the following pieces of chat logs as context to provide your responses.
        Make a reasonable assumption based on the context if you are unsure.
        Use ten sentences maximum and keep the answer concise.
        Question: {question}
        Context: {context}
    """)
    return prompt.invoke({"question": query, "context": context}).to_messages()
