import os
import openai
from chromadb import HttpClient
from dotenv import load_dotenv

load_dotenv()

# API Key for OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# ChromaDB Docker connection settings
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8001))
print(f"Connecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}...")
# Connect to ChromaDB running in Docker
client = HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# Get or create vector DB collections
rag_collection = client.get_or_create_collection(name="rag_docs")
intent_collection = client.get_or_create_collection(name="intent_docs")


def get_embedding(text: str) -> list:
    """Generate embedding using OpenAI."""
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def parse_md_file(file_path):
    """Extract records from .md file where each record starts with ##"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    records = []
    chunks = content.split("## ")
    for chunk in chunks:
        if chunk.strip():
            lines = chunk.strip().split("\n")
            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip()
            if body:
                records.append({"title": title, "content": body})
    return records


def load_documents(md_dir: str):
    """Loads .md files into appropriate collections based on filename."""
    for filename in os.listdir(md_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(md_dir, filename)
            records = parse_md_file(file_path)
            is_intent = filename.lower() == "intent.md"
            collection = intent_collection if is_intent else rag_collection

            for i, record in enumerate(records):
                doc_id = f"{filename}_{i}"
                content = f"{record['title']}\n{record['content']}"
                try:
                    existing = collection.get(ids=[doc_id])
                    if existing and len(existing["ids"]) > 0:
                        continue
                except:
                    pass

                embedding = get_embedding(content)
                collection.add(
                    documents=[content],
                    embeddings=[embedding],
                    ids=[doc_id],
                    metadatas=[{"file": filename, "title": record["title"]}]
                )
    print("✅ Markdown documents embedded and loaded into ChromaDB.")


def get_doc_context(question: str) -> str:
    """Get one top matching doc per each doc file and combine them."""
    embedding = get_embedding(question)
    target_files = ["filters.md", "columns.md", "examples.md", "metrics.md"]
    combined_docs = []

    for fname in target_files:
        result = rag_collection.query(
            query_embeddings=[embedding],
            n_results=1,
            where={"file": fname},
            include=["documents"]
        )
        docs = result.get("documents", [[]])[0]
        if docs:
            combined_docs.append(docs[0])

    return "\n\n".join(combined_docs) if combined_docs else "No relevant documents found."


def get_intent_context(question: str, top_k: int = 3) -> str:
    """Query only from intent.md collection."""
    embedding = get_embedding(question)
    results = intent_collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return "\n\n".join(results["documents"][0]) if results["documents"][0] else "No intent documents found."


def is_filtering_question(question: str) -> bool:
    keywords = ["filter", "filtering", "filtered", "filter out", "filter data"]
    q = question.lower()
    return any(k in q for k in keywords)


def initialize(md_dir: str):
    reset = os.getenv("RESET_CHROMA_DB", "false").lower() == "true"
    try:
        if reset:
            print("🧹 Resetting ChromaDB collections...")
            if rag_collection.count() > 0:
                all_ids = rag_collection.get()["ids"]
                rag_collection.delete(ids=all_ids)

            # Delete all from intent_collection
            if intent_collection.count() > 0:
                all_ids = intent_collection.get()["ids"]
                intent_collection.delete(ids=all_ids)
            print("✅ Collections reset.")
            load_documents(md_dir)
        elif rag_collection.count() == 0 or intent_collection.count() == 0:
            print("📂 Vector DB is empty. Loading Markdown documents...")
            load_documents(md_dir)
        else:
            print("🗃️ Vector DB already populated.")
    except Exception as e:
        #load_documents(md_dir)
        print("❌ Error during ChromaDB initialization:", str(e))




