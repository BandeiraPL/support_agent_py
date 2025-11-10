#criação da api / substitui o main/
#bash na pasta do cod / 

from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 🔧 Carregar variáveis de ambiente
load_dotenv()

app = FastAPI(title="PDF Agent API")

# 🧠 Carregar FAISS e LLM
vectorstore_path = os.getenv("VECTORSTORE_FOLDER", "./vectordb/faiss_index")

print("📦 Carregando FAISS index...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local(
    vectorstore_path,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 🧩 Prompt atualizado — para forçar resposta explicativa + fonte
prompt = ChatPromptTemplate.from_template(
    """Você é um assistente que responde perguntas com base em documentos PDF.
Leia o contexto abaixo e elabore uma resposta clara, completa e direta à pergunta.
Ao final da resposta, cite a fonte (nome do PDF e página), caso disponível.

Contexto:
{context}

Pergunta:
{question}

Responda de forma explicativa, e no final acrescente algo como:
'Fonte: [nome do arquivo], página X'."""
)

# 🔗 Função que adiciona metadados visíveis, mas de forma leve
def format_docs(docs):
    formatted = []
    for d in docs:
        source = d.metadata.get("source", "Fonte desconhecida")
        page = d.metadata.get("page", "página desconhecida")
        formatted.append(
            f"Trecho do arquivo {os.path.basename(source)}, página {page}:\n{d.page_content}"
        )
    return "\n\n".join(formatted)

# 🔗 Montagem do pipeline
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 📩 Modelo da requisição
class QuestionRequest(BaseModel):
    question: str

# 📤 Endpoint principal
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    resposta = chain.invoke(request.question)
    return {"answer": resposta.content}
