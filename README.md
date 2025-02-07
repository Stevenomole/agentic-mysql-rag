# Agentic RAG README

## Overview
This repository provides a simple agent that allows users to query a MySQL database using natural language. It leverages LangChain components for prompt handling and LLM interaction, while Streamlit provides an intuitive user interface. 

The database itself is not included because it contains proprietary data that was purchased, but you can easily substitute your own database in order to replicate or extend this functionality.

## Requirements
1. **Python 3.9 or above**  
   Please ensure that you have a compatible Python version installed before proceeding.

2. **Dependencies**  
   The primary libraries employed are:
   - `langchain_community.utilities`  
   - `langchain_ollama`  
   - `langchain_core.prompts`  
   - `streamlit`  
   - `mysql-connector-python` or another MySQL driver  
   
   You will also need an LLM model that can be accessed through `ChatOllama`.

3. **MySQL Database**  
   An operational MySQL database, such as a local instance or a remote server, is required. The code relies on a connection URI that includes credentials. Replace these details with your own values.

4. **LLM Model**  
   This agent uses `ChatOllama(model="llama3.1")`. You may update the model name or configuration based on your local environment or available resources.

## Installation
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/stevenomole/agentic-mysql-rag.git
   cd agentic-mysql-rag
   ```

2. **Create and Activate a Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database Credentials**  
   Update the MySQL URI in the `connectDatabase()` function to match your database credentials, including the username, password, host, and database name.

5. **Adjust LLM Configuration**  
   Review the `llm = ChatOllama(model="llama3.1")` line. Modify the model name or connection logic as necessary.

## Usage
1. **Run the Streamlit Application**  
   ```bash
   streamlit run path_to_your_python_file.py
   ```
   Replace `path_to_your_python_file.py` with the actual Python file name, if you have renamed it.

2. **Connect to the Database**  
   - When prompted in the sidebar, click the **Connect** button to establish a database connection.  
   - If successful, Streamlit will display a confirmation message.

3. **Enter Queries**  
   - Use the main chat input field to ask questions in natural language.  
   - Observe the application generate an SQL query, run it against your database, and provide a descriptive answer.

4. **Analyze Results**  
   - The agent returns an explanation intended for data analysts.  
   - Read through the response to understand patterns or insights drawn from your query results.
