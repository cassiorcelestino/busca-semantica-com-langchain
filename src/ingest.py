import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ingestão de dados conforme explicado na aula do langchain - Data Loading e RAG > enriquecendo documentos.
def ingest_pdf():
    pdf_path = os.getenv("PDF_PATH")
    database_url = os.getenv("PGVECTOR_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
    max_chunks = int(os.getenv("MAX_CHUNKS", "0"))

   # usando uma anotação mais simples. O Wesley usou uma outra com for que achei dificil pra ler.
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY nao foi definida no .env")
    #caminho do PDF (PATH) definido no .env . Melhor do que deixar no código.
    if not pdf_path:
        raise ValueError("PDF_PATH nao foi definida no .env")
    if not database_url:
        raise ValueError("PGVECTOR_URL nao foi definida no .env")
    if not collection_name:
        raise ValueError("PG_VECTOR_COLLECTION_NAME nao foi definida no .env")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Arquivo PDF nao encontrado: {pdf_path}")

    print("Carregando PDF...")
    # esse comando a seguir do PYPDFLoader ... load () ja percorre internamente as paginas do PDF e devolve uma lista de paginas
    pages = PyPDFLoader(pdf_path).load()

    # tambem tem um laço interno, percorre essa lista internamente para quebrar cada pagina em chunks.
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splits.split_documents(pages)
    if max_chunks > 0:
        chunks = chunks[:max_chunks]

    print("=" * 50 )
    print(f"Paginas carregadas: {len(pages)}")
    print(f"Chunks em uso: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True,
    )

    store.add_documents(chunks)

    print("Ingestao concluida com sucesso.")


if __name__ == "__main__":
    ingest_pdf()
