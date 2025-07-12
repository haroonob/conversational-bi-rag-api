import asyncio
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from decimal import Decimal
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import json
from fastapi import Query
from sqlalchemy import create_engine, text
from datetime import datetime, date
from fastapi.middleware.cors import CORSMiddleware

# Assume your rag_retriever.py provides these functions
from .rag_retriever import get_doc_context, get_intent_context, initialize

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
DATABASE_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@postgres:5432/ecommerce")
engine = create_engine(DATABASE_URL)

# Load RAG documents once at startup
initialize("docs")

system_prompt = """
You are a PostgreSQL SQL query generator for the `orders` table. Your response should be a valid, pure PostgreSQL SQL query without any markdown, code fences, or extra formatting—do not include any triple backticks (```).

Use the contextual information from RAG documents—including filters, metrics, and schema—to build accurate and valid SQL queries. Remove any unnecessary characters such as triple backticks.

Guidelines:

- Always refer to the RAG files for available metrics, filters, and column definitions.
- Use DATE_TRUNC for any temporal grouping (e.g., by month).
- For quarterly comparisons, use this filter:

  InvoiceDate BETWEEN DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '3 months'
                 AND DATE_TRUNC('quarter', CURRENT_DATE)

Response Format:

1. For intent = 'graph':
   - Return a multi-row query with exactly two columns.
   - Include at least one grouping column (e.g., month, country).
   - Include one or more numeric metrics.
   - Use clear column aliases (e.g., AS total_revenue).

2. For intent = 'text':
   - Return a single-row, single-column query.
   - Use an alias for the output column.

Make sure all queries strictly follow PostgreSQL syntax and logic consistent with the RAG content.

Remember: Do NOT include any triple backticks or markdown code formatting in your response. Return only the raw SQL query.
Remember : Do Not use quote around column names or table names. 

"""

def serialize_row(row, columns):
    name = row[0]
    value = row[1] if len(row) > 1 else None

    if isinstance(name, (datetime, date)):
        name = name.strftime("%B %Y")

    if isinstance(value, Decimal):
        value = float(value)

    return {"name": name, "value": value}

@app.get("/api/query")
async def sse_query(question: str = Query(...)):
    if not question:
        return {"error": "Missing 'question' in request body"}

    context = get_doc_context(question)
    print(f"Context for question '{question}': {context}")
    prompt = f"""{context}\nUse the 'orders' table with columns:\n\nQuestion:\n{question}"""

    # Detect intent (graph or text)
    intent_context = get_intent_context(question)
    intent_obj = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Give one word response: either 'graph' or 'text' depending on whether query returns multiple rows or a single value."
            },
            {
                "role": "user",
                "content": f"Original question: {question}\nAdditional context: [{intent_context}]"
            }
        ]
    )
    intent = intent_obj.choices[0].message.content.strip().lower()
    if intent not in ("graph", "text"):
        intent = "text"

    prompt_with_intent = prompt + f"\nIntent: {intent}\n"

    # Generate SQL query with streaming from OpenAI
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_with_intent}
        ],
        stream=True
    )

    async def event_stream():
        sql_fragments = []
        try:
            yield f"data: [INFO] Generating SQL...\n\n"

            # Stream SQL generation word by word
            async for chunk in response:
                delta = chunk.choices[0].delta.content or ""
                sql_fragments.append(delta)
                for word in delta.split():
                    yield f"data: [SQL] {word}\n\n"
                    await asyncio.sleep(0.02)

            sql = ''.join(sql_fragments)

            # Basic SQL safety check
            lower_sql = sql.lower()
            if any(danger in lower_sql for danger in ["drop", "delete", "update", "insert"]):
                yield f"data: ERROR::Unsafe SQL detected.\n\n"
                return

            yield f"data: [INFO] Executing SQL...\n\n"
            print(lower_sql,intent) 
            # Execute SQL query
            with engine.connect() as conn:
                result = conn.execute(text(sql))
                rows = result.fetchall()
                columns = result.keys()

            if intent == "graph":
                data = [serialize_row(row, columns) for row in rows]
                meta = {
                    "intent": "graph",
                    "graphType": "bar",
                    "data": data
                }
                yield f"data: {json.dumps(meta)}\n\n"

            else:
                v = rows[0][0]
                yield f"data: [INFO] Generating final answer...\n\n"

                # Get descriptive text answer
                singlevalue_answer = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Use the question and value after it, answer professionally in descriptive text. it should be a one liner short answer"},
                        {"role": "user", "content": f"{question}: {v}"}
                    ]
                )
                answer_text = singlevalue_answer.choices[0].message.content.strip()

                meta = {
                    "intent": "text",
                    "graphType": None,
                    "data": None
                }
                yield f"data: {json.dumps(meta)}\n\n"

                for word in answer_text.split():
                    yield f"data: {word}\n\n"
                    await asyncio.sleep(0.03)

        except Exception as e:
            yield f"data: ERROR::{str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
