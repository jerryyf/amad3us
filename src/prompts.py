from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate

def rag_prompt(query: str, context: str) -> list[BaseMessage]:
    prompt = PromptTemplate.from_template("""
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, say you don't know, but make a reasonable assumption based on the context.
        Use ten sentences maximum and keep the answer concise.
        Question: {question}
        Context: {context}
    """)
    return prompt.invoke({"question": query, "context": context}).to_messages()
