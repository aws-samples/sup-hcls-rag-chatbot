# genai-immersion-series-rag-demo

This solution demonstrates how you can create a simple generative AI chatbot that uses Retreival Augmented Generation (RAG) to ask questions of specific documents.  The solution leverages Amazon Bedrock and the Claude Instant model from Anthropic as the foundation model (FM) to query documents of your choice.

## Installation Instructions

Python, the Python package installer pip, and virtual environment manager, virtualenv, are required for this solution. Windows installations of compatible Python versions include these tools. On Linux, pip and virtualenv may be provided as separate packages in your package manager. Alternatively, you may install them with the following commands: 
```
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv
```

Clone this solution to your workspace with the command
```
git clone https://gitlab.aws.dev/colgc/genai-immersion-series-rag-demo
cd genai-immersion-series-rag-demo
```
After cloning the solution, create and activate the project's virtual environment. This allows the project's dependencies to be installed locally in the project folder, instead of globally. 
```
virtualenv .venv
source .venv/bin/activate
```
After activating your virtual environment, install the dependencies:
```
python -m pip install -r requirements.txt
```
NOTE: Activate the project's virtual environment whenever you start working on it. Otherwise, you won't have access to the modules installed there, and modules you install will go in the Python global module directory (or will result in a permission error). 

## Usage Instructions

This solution requires that you create a set of embeddings based on your document and store them in a vector database.  Don't worry, it sounds harder than it is!  This solution supports docx, pdf, txt, json & csv using document loaders from Langchain.  See the ![Langchain documentation](https://python.langchain.com/docs/modules/data_connection/document_loaders/) for any additional loaders you may wish to use.  Let's get started:

1. Update the `credentials_profile_name` & `region_name` in the `create_index.py` & `bedrock_rag_demo_lib.py` files to match your settings.
2. Drop the documents you want to experiment with in the ![docs](/docs) folder.
3. In your virtual environment that you initialized above, run `python create_index.py` to create the embeddings and store them in a local vector database using the opensource tool ![Chromadb](https://www.trychroma.com/).
4. Once the vector database has been created, you can run the chatbot interface, powered by the ![Streamlit](https://streamlit.io/) library.  Run the command `streamlit run bedrock_rag_demo_app.py --server.port 8080` to start the chatbot interface.
5. Open a browser to the address, such as <http://localhost:8080> and ask your questions!

The `bedrock_rag_demo_lib.py` file contains the prompt sent to Claude.  Feel free to experiemnt by adjusting the `input_text` variable to suit your particular needs, or just modify it to see how it impacts the response from Claude.  Enjoy!