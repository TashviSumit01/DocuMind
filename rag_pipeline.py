from langchain_community.document_loaders import PyPDFLoader,WebBaseLoader,TextLoader,Docx2txtLoader,CSVLoader,UnstructuredExcelLoader,UnstructuredEmailLoader
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import PIL.Image

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def create_vectorstore(source,source_type):
    if source_type == "pdf":
        loader = PyPDFLoader(source)
    elif source_type == "url":
        loader = WebBaseLoader(source)
    elif source_type == "text":
        loader = TextLoader(source)
    elif source_type == "xlsx" :
        loader = UnstructuredExcelLoader(source)
    elif source_type == "email":
        loader = UnstructuredEmailLoader(source)
    elif source_type == "docx":
        loader = Docx2txtLoader(source)
    elif source_type == "csv":
        loader = CSVLoader(source)    
    elif source_type in ["png","jpg","jpeg"]:
        import google.generativeai as genai
        from langchain_core.documents import Document
        import base64
        genai.configure(api_key = GOOGLE_API_KEY)
        model =genai.GenerativeModel("gemini-2.5-flash")

        with open(source, "rb") as f:
            image_data = f.read()

        image_b64 = base64.b64encode(image_data).decode()

        response = model.generate_content([
            "Extract and describe all text,data, and infromation from this image in detail.",
            {"mime_type":f"image/{source_type}", "data": image_b64}
        ]) 

        text_content = response.text
        documents = [Document(page_content=text_content, metadata={"source": source})]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        chunks=text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks,embeddings)
        return vectorstore  
               
    else:
        raise ValueError(f"Unsupported source type: {source_type}")

    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)      
    chunks = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore= FAISS.from_documents(chunks,embeddings)
    return vectorstore
  
def get_answer(question,vectorstore):
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    
    if vectorstore is None:
        from langchain_core.messages import SystemMessage, HumanMessage
        messages = [
            SystemMessage(content="""You are DocuMind, a friendly AI document assistant.
            You are GenZ and millennial enough to understand everything the user says.
            You help users read, understand and explain documents.
            When asked your name, say you are DocuMind.
            When asked what you do, explain you help people understand their documents.Be friendly, warm and conversational!"""),
            HumanMessage(content=question)
        ]
        response = llm.invoke(messages)
        return response.content, []

    relevant_chunks = vectorstore.similarity_search(question,k=10)
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])

    prompt=f"""You are DocuMind, a friendly AI document assistant.
The user has uploaded a document. Use the context below to answer their question.

IMPORTANT RULES:
1. If the question is about the document content → answer from the document context below
2. If the question is a general question NOT related to the document → answer from your general knowledge directly, don't mention the document
3. Never say "there is no information" for general knowledge questions

    Document text:
    {context}

    Question:{question}
    
    Answer:"""


    response = llm.invoke(prompt)
    answer = response.content
    sources = [chunk.metadata["source"] for chunk in relevant_chunks]
    return answer, sources