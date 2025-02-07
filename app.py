from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

#from dotenv import load_dotenv
#from langchain_openai import ChatOpenAI

def connectDatabase():
    mysql_uri = f"mysql+mysqlconnector://root:Mysql44%40@localhost:3306/bitcoin_data"
    st.session_state.db = SQLDatabase.from_uri(mysql_uri)

def runQuery(query):
    return st.session_state.db.run(query) if st.session_state.db else "Please connect to database"

def getDatabaseSchema():
    return st.session_state.db.get_table_info() if st.session_state.db else "Please connect to database"

def getLLMQueryResponse(question):
    template = """Below is the schema of mysql database. Please answer user's questions in the form of 
    SQL query by looking into the schema. Only provide the one and only one SQL query and nothing else.
    If more than one question was asked, find a way to aggregate it into one SQL. Thank you!

    {schema}

    question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({
    "question": question,
    "schema": getDatabaseSchema()
    })

    return response.content

def getLLMResponse(question, result):
    template2 = """Please convert the results in a descriptive way that is useful to a data analyst. Don't add additional
    information. Ensure to answer based on what the original prompt was. Thank you!

    question: {question}
    result: {result}
    """
    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = prompt2 | llm

    response = chain2.invoke({
        "result": result,
        "question": question
    })

    return response.content

llm = ChatOllama(model="llama3.1")

# Using streamlit to interface with the agent
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False

st.set_page_config(
    page_icon="💬",
    page_title="Chat with MySQL DB",
    layout="centered"
)

with st.sidebar:
    st.title("Connect to DB")
    connectButton = False
    if not st.session_state.db_connected:
        connectButton = st.button("Connect") 
    else:
        st.success("Database Connected!")

if connectButton:
    try:
        connectDatabase()
        st.session_state.db_connected = True
        st.success("DB Connected!")
    except Exception as e:
        st.error(f"Failed to connect to database: {str(e)}")

question = st.chat_input("What is your prompt?")

if question:
    if not st.session_state.db_connected:
        st.error("Please connect to the database first!")
    else:
        st.chat_message("user").markdown(question)
        
        with st.spinner("Generating SQL query..."):
            try:
                sql_query = getLLMQueryResponse(question)
                st.chat_message("assistant").markdown("Generated SQL Query:")
                st.chat_message("assistant").markdown(f"```sql\n{sql_query}\n```")
                
                with st.spinner("Executing query..."):
                    result = runQuery(sql_query)
                    
                with st.spinner("Analyzing results..."):
                    response = getLLMResponse(question, result)
                    st.chat_message("assistant").markdown(response)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
