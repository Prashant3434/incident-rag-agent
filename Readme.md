🚨 Incident RAG Agent

An intelligent Retrieval-Augmented Generation (RAG) Agent designed to assist engineering, DevOps, and SRE teams with incident response, root cause analysis (RCA), and automated troubleshooting. By indexing historical incident reports, runbooks, and system logs into a vector store, this agent uses Large Language Models (LLMs) and custom tool calling to provide context-aware resolutions in real time.

✨ Key Features

📚 Automated Knowledge Ingestion: Converts historical incident records and technical runbooks into searchable vector embeddings (create_embadding.py).

🤖 Agentic Tool Execution: Equips the LLM with specialized retrieval and diagnostic tools to query past incidents and system states (llm/tools.py).

🧠 Customizable Persona & Guardrails: Driven by a dedicated, easily modifiable system prompt (system_prompt.txt) to ensure accurate, hallucination-free SRE guidance.

⚡ Modular Architecture: Clean separation between embedding pipelines, core LLM orchestration, tool definitions, and the main execution interface.

📂 Project Structure

incident-rag-agent/
├── llm/
│   ├── __init__.py          # Package initializer for the LLM module
│   ├── llm.py               # Core LLM client configuration, agent setup, and inference logic
│   └── tools.py             # Custom tools for vector search, incident lookup, and diagnostics
├── .gitignore               # Git ignore rules (environment variables, cache, vector DB files)
├── create_embadding.py      # Script to parse incident data, generate embeddings, and build the vector index
├── main.py                  # Main entry point to run the Incident RAG Agent
├── system_prompt.txt        # System instructions defining the agent's behavior and incident workflow
└── README.md                # Project documentation


🛠️ Prerequisites

Python: 3.9 or higher

LLM API Key: An active API key for your configured LLM provider (e.g., OpenAI, Google Gemini, Anthropic, or local Ollama instance)

Vector Store / Embeddings: Configured within create_embadding.py (e.g., ChromaDB, FAISS, Pinecone, or Qdrant)

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/Prashant3434/incident-rag-agent.git
cd incident-rag-agent


2. Create a Virtual Environment

python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate


3. Install Dependencies

Install the required packages (or create a requirements.txt based on your imports):

pip install -r requirements.txt


(Note: If you haven't generated a requirements.txt yet, you can create one from your active environment using pip freeze > requirements.txt.)

4. Configure Environment Variables

Create a .env file in the root directory and add your required credentials:

# Example configuration (update keys based on your llm/llm.py implementation)
OPENAI_API_KEY=your_api_key_here
# GEMINI_API_KEY=your_api_key_here
# VECTOR_DB_PATH=./vector_store


💻 Usage

Step 1: Generate Embeddings

Before running the agent, ingest your incident dataset or runbooks and populate the vector database:

python create_embadding.py


Step 2: Run the Incident Agent

Launch the main application to start querying incidents and interacting with the RAG agent:

python main.py


⚙️ Customization

Adjusting Agent Behavior: Edit system_prompt.txt to refine how the agent formats Root Cause Analyses (RCAs), prioritizes severity levels, or cites historical tickets.

Adding New Capabilities: Define new Python functions in llm/tools.py to allow the agent to fetch live metrics, query ticketing systems (like Jira or ServiceNow), or search external documentation.

Switching Models: Update the model configuration inside llm/llm.py to test different foundation models or embedding providers.

🤝 Contributing

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License

This project is open-source and available under the MIT License.
