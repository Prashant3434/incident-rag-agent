from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb
from llm.llm import LLM
import json

load_dotenv()

llm = LLM(
    base_url=os.getenv('LLM_BASE_URL'),
    api_key=os.getenv("API_KEY")
)


db = chromadb.PersistentClient(
    path=os.getenv("RAG_DB_PATH")
)

collection = db.get_collection(
    name=os.getenv("RAG_DB_COLLECTION")
)

def search_incident(query):
    # user_description = input("Please Provide the description of the issue: ")

    embedding = llm.client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=[query]
    )

    matches = collection.query(
        query_embeddings=[embed.embedding for embed in embedding.data],
        n_results=2
    )
    # print(matches)
    return [
        f"""
        Incedent details:
            "incident_number":{match['number']}
            "short_description":{match['short_description']},
            "description":{match['description']},
            "close_notes":{match['close_notes']}

        """
        for match in matches['metadatas'][0] 
    ]
    # print(match['metadatas'][0]['close_notes'])



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

messages = [
    {
        "role":"system",
        "content":"""
        You are a helpful ServiceNow incident support assistant.

        Understand the user's query and call the incident search tool when relevant information is needed.
        Use only the retrieved incident data: description, short description, and close notes.
        Answer using relevant incidents and provide up to 3 possible solutions supported by the retrieved data.
        Do not invent solutions, assume facts, or use knowledge outside the retrieved data.
        If the retrieved information is insufficient to answer, respond exactly: "No sufficient information exists to answer this query."
        Keep answers concise, clear, and actionable.
        use citetion for your response
        """
    }
]

tool_registry = {
    "search_incidents":search_incident
}

def tool_runner(tool_name,arguments):
    if tool_name not in tool_registry:
        return "No such tool exist"
    
    if tool_name == "search_incidents":
        value = tool_registry[tool_name](arguments["query"])
        # print(arguments)
        return json.dumps(value)



temp_messages = [message for message in messages]
while True:
    query = input("Query >>> ")
    
    if query == "exit":
        break
    
    if query == "clear":
        messages = [message for message in temp_messages]
        print("AI >>> Context is clear")
        continue
    
    messages.append(
        {
            "role":"user",
            "content":query
        }
    )
    
    while True:
        response = llm.call(
            messages=messages,
            tools = tools,
            model_name = os.getenv("MODEL_NAME")
        )

        if response["content"] is not None and response["content"] != "":
            messages.append(response)
            print("AI response >> ",response["content"])
            break
        
        if response["tool_calls"]:
            messages.append(response)
            for tool in response["tool_calls"]:
                print("Tool >>>",tool["function"]["name"]," is running")
                tool_res = tool_runner(tool["function"]["name"],json.loads(tool["function"]["arguments"]))
                # print("Tool >>> ",tool_res)
                messages.append(
                    {
                        "role":"tool",
                        "id":tool["id"],
                        "content":tool_res
                    }
                )
        