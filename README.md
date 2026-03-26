# Desafio MBA Engenharia de Software com IA - Full Cycle

Projeto de busca semântica com LangChain, PostgreSQL/pgvector e Google Gemini.

## Objetivo

Executar um chat que responde perguntas com base no PDF carregado no banco vetorial.

## Entregável (requisito do projeto)

1. Repositório público no GitHub
2. Código-fonte completo
3. README com instruções claras de execução

## Pré-requisitos

- Python 3.12
- Docker Desktop em execução
- Chave de API Google em GOOGLE_API_KEY

## Passo a passo (execução)

1. Criar e ativar ambiente virtual:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Criar arquivo de ambiente:

```bash
copy .env.example .env
```

4. Preencher o .env:

```env
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=document_chunks
PDF_PATH=./document.pdf
MAX_CHUNKS=0
```

5. Subir banco de dados:

```bash
docker compose up -d
docker compose ps
```

6. Ingerir o PDF no banco vetorial:

```bash
python src\ingest.py
```

Saída esperada:

```text
Carregando PDF...
==================================================
Paginas carregadas: XX
Chunks em uso: XX
Ingestao concluida com sucesso.
```

7. Iniciar chat:

```bash
python src\chat.py
```

Saída esperada:

```text
==================================================
Chat iniciado. Digite uma pergunta ou 'sair' para encerrar.
PERGUNTA:
```

Para encerrar o chat, digite sair ou use Ctrl+C.

## Nota sobre MAX_CHUNKS

- MAX_CHUNKS=0: ingere todos os chunks do PDF (modo oficial)
- MAX_CHUNKS=3: ingere apenas 3 chunks (modo teste, economiza quota)
- Para os testes documentados neste projeto, foi utilizado MAX_CHUNKS=3 devido ao limite de quota de uso do modelo.

## Comportamento esperado

- O sistema responde apenas com base no conteúdo do PDF carregado.
- Perguntas fora do contexto retornam: "Nao tenho informacoes necessarias para responder sua pergunta."
- Sem Docker ativo, ingest.py e chat.py encerram com mensagem de erro.

## Evidência de teste (execução real)

Teste realizado com o chat em execução e base vetorial já ingerida.

```text
==================================================
Chat iniciado. Digite uma pergunta ou 'sair' para encerrar.
PERGUNTA: Qual o faturamente da empresa ALFA IA Industria
==================================================
RESPOSTA: R$ 548.789.613,65

PERGUNTA: A empresa Alta Midia foi criada em que ano?
==================================================
RESPOSTA: 1978

PERGUNTA: Qual o faturament da Atlas Gás Serviços
==================================================
RESPOSTA: R$ 55.110.243,34

PERGUNTA: Em que pais está localizado a empresa Atlas Biotech S.A
==================================================
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

PERGUNTA: Qual a capital da França
==================================================
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

PERGUNTA: o Faturamento da Aliança Hotelaria EPP é de R$ 4.440.178,43?
==================================================
RESPOSTA: Sim, o faturamento da Aliança Hotelaria EPP é de R$ 4.440.178,43.

PERGUNTA: Tenho dúvida qual empresa é mais antiga a Atlas Construtora S.A ou a Atlas Higiene Indústria?
==================================================
RESPOSTA: Atlas Construtora S.A. foi fundada em 1939 e Atlas Higiene Indústria foi fundada em 1939.
```

