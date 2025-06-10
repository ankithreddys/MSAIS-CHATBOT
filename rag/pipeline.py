from langchain_openai import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def build_rag_pipeline(GAITOR_API_KEY, vector_store, model="llama-3.1-70b-instruct"):
    llm = ChatOpenAI(
        temperature=0.7,
        model=model,
        openai_api_base="https://api.ai.it.ufl.edu",
        openai_api_key = GAITOR_API_KEY
    )

    retriever = vector_store.as_retriever(search_kwargs = {"k":25})

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    return conv_chain