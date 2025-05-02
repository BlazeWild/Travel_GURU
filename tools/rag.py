# rag.py
from typing import List
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

async def create_rag(urls: List[str]) -> FAISS:
    from search import get_web_content
    all_docs = []
    for url in urls:
        docs = await get_web_content(url)
        all_docs.extend(docs)
    return await create_rag_from_documents(all_docs)

async def create_rag_from_documents(docs: List[Document]) -> FAISS:
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

async def search_rag(query: str, vectorstore: FAISS) -> List[Document]:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever.get_relevant_documents(query)