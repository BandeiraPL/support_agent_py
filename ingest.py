import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

pdf_folder = Path(os.getenv("PDF_FOLDER"))
vectorstore_path = os.getenv("VECTORSTORE_FOLDER")

def load_pdfs(folder):
    docs = []
    pdf_files = list(folder.glob("*.pdf"))
    
    print(f"🔍 Encontrados {len(pdf_files)} PDFs em '{folder}'")
    
    for file in pdf_files:
        try:
            print(f"📄 Carregando: {file.name}")
            loader = PyPDFLoader(str(file))
            loaded = loader.load()
            if not loaded:
                print(f"⚠️ {file.name} - Nenhum texto extraído.")
            else:
                print(f"✅ {file.name} - {len(loaded)} páginas carregadas")
            docs.extend(loaded)
        except Exception as e:
            print(f"❌ Erro ao carregar {file.name}: {e}")
    
    print(f"📚 Total de documentos carregados: {len(docs)}")
    return docs

def main():
    print("🔍 Carregando PDFs...")
    raw_docs = load_pdfs(pdf_folder)

    print("✂️ Dividindo texto em pedaços...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(raw_docs)

    print("🔎 Gerando embeddings com HuggingFace...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("💾 Criando FAISS index...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(vectorstore_path)

    print(f"✅ Vector store salvo em: {vectorstore_path}")

if __name__ == "__main__":
    main()
