from openai import OpenAI
import chromadb
import json
import os



def search_incidents(query):
    
    client = OpenAI(
        base_url=os.getenv('EMBED_BASE_URL'),
        api_key=os.getenv("EMBED_API_KEY")
    )

    embedding = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=[query]
    )

    db = chromadb.PersistentClient(
        path=os.getenv("RAG_DB_PATH")
    )

    collection = db.get_collection(
        name=os.getenv("RAG_DB_COLLECTION")
    )


    matches = collection.query(
        query_embeddings=[embed.embedding for embed in embedding.data],
        n_results=3
    )

    return {
        match['number']:{
            "short_description":match['short_description'],
            "description":match['description'],
            "close_notes":match['close_notes']
        }
        for match in matches['metadatas'][0] 
    }







tools = [
    {
        "type": "function",
        "function": {
            "name": "search_incidents",
            "description": (
                "Search the ServiceNow incident knowledge base for incidents "
                "relevant to the user's query. Returns an array of matching "
                "incidents, each containing a short description, full description, "
                "and close notes describing the resolution. Use this tool when "
                "incident-specific information or troubleshooting solutions are needed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The user's incident-related question or problem "
                            "to search for, including symptoms or error messages."
                        )
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]