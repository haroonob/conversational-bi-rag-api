from app.rag_retriever import initialize, get_doc_context, get_intent_context

# Initialize once (load or skip if DB exists)
initialize("docs")

# Now query:
question = "Show total revenue trends by month for the last quarter.?"
print("📄 Doc Context:\n", get_doc_context(question))
print("\n🎯 Intent Context:\n", get_intent_context(question))
