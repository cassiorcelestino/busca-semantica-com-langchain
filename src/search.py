import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

NO_CONTEXT_ANSWER = "Nao tenho informacoes necessarias para responder sua pergunta."

load_dotenv()
for k in ("GOOGLE_API_KEY", "PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k):
        raise ValueError(f"Variável de ambiente {k} não está definida")

pgvector_url = os.getenv("PGVECTOR_URL")
if not pgvector_url:
    raise ValueError("Variável de ambiente PGVECTOR_URL não está definida")

# query = "Tell me qq coisa"
embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001"))

store = PGVector (
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=pgvector_url,
        use_jsonb=True )

def search_prompt(question=None):
    results = store.similarity_search_with_score(question, k=10)
    print ("=" * 50)
    contexto = "\n\n".join([doc.page_content for doc, _score in results])
    if not contexto.strip():
        return {
            "results": results,
            "contexto": contexto,
            "prompt": "",
            "answer": NO_CONTEXT_ANSWER,
        }

    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_CHAT_MODEL", "gemini-2.5-flash-lite"),
        temperature=0,
    )
    response = llm.invoke(prompt)

    answer = response.content.strip() if hasattr(response, "content") else str(response)
    return {
        "results": results,
        "contexto": contexto,
        "prompt": prompt,
        "answer": answer,
    }






PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
    "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.
EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

