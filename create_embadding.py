# print(incident['records'][0]['close_notes'],end="\n")
# print(incident['records'][0]['number'])
# print(incident['records'][0]['state'])
# print(incident['records'][0]['short_description'])
# print(incident['records'][0]['description'])


from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os
import json

load_dotenv()

RAGdb = chromadb.PersistentClient(path=os.getenv("RAG_DB_PATH"))

collection = RAGdb.get_or_create_collection(
    name=os.getenv("RAG_DB_COLLECTION"),
)

client = OpenAI(
    base_url=os.getenv("EMBED_BASE_URL"),
    api_key=os.getenv("API_KEY")
)

with open("./valgenesis_incident.json","r",encoding="utf-8") as file:
    incidents = json.load(file)['records']


template ="""
Short Description: {short_description},
Description: {description}
"""


documents=[
    {
    "number":incident['number'],
    "short_description":incident['short_description'],
    "description":incident['description'],
    "close_notes":incident['close_notes']
    }
    for incident in incidents
]

doc_for_embedding = [
    template.format(
        short_description=i['short_description'],
        description=i['description']
    )
    for i in documents
] 

batch_size = 20

for i in range(0,len(documents),batch_size):
    # print(documents[i:i+batch_size])
    print("[embedding] start from: ",i," to:",i+batch_size)
    embeddings = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=doc_for_embedding[i:i+batch_size]
    )

    collection.upsert(
        ids=[
            str(doc['number']) for doc in documents[i:i+batch_size]
        ],
        metadatas=[doc for doc in documents[i:i+batch_size]],
        embeddings=[
        embed.embedding for embed in embeddings.data
        ]
    )



