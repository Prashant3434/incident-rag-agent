from openai import OpenAI
from dotenv import load_dotenv
from llm.llm import LLM
from llm.tools import tools, search_incidents
import json
import os

load_dotenv()



llm = LLM(
    base_url=os.getenv('LLM_BASE_URL'),
    api_key=os.getenv("API_KEY")
)



messages = [
    {
        "role":"system",
        "content":"""
        You are a ServiceNow incident support assistant.

        Search past incidents relevant to the user's issue. Use only their short description, description, and close notes.

        From the retrieved incidents, provide up to 3 actual solutions or workarounds that previously resolved similar issues. Write each as a direct action the user can take, not as a summary of what an incident says.

        Do not invent, infer, or use external knowledge. Every solution must be explicitly supported by retrieved incident data and include a citation.

        If no supported solution exists, respond exactly:
        "No sufficient information exists to answer this query."

        Output: 
        Solution 1: <direct solution/workaround> <citation>
        Solution 2: <direct solution/workaround> <citation>
        Solution 3: <direct solution/workaround> <citation>
        """
    }
]

tool_registry = {
    "search_incidents":search_incidents
}

def tool_runner(tool_name,arguments):
    if tool_name not in tool_registry:
        return {
            "error":"invalid tool call"
        }
    
    if tool_name == "search_incidents":
        value = tool_registry[tool_name](arguments["query"])
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
    
        if response["content"]:
            messages.append(response)
            print("AI response >> ",response["content"])
            break
        
        if response["tool_calls"]:

            messages.append(response)
            tool_run = []
            for tool in response["tool_calls"]:
                print("Tool >>>",tool["function"]["name"]," is running")
                tool_res = tool_runner(tool["function"]["name"],json.loads(tool["function"]["arguments"]))
                messages.append(
                    {
                        "role":"tool",
                        "tool_call_id":tool["id"],
                        "name":tool["function"]["name"],
                        "content":tool_res
                    }
                )
        