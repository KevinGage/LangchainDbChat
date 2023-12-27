from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import Database
from code_llm import CodeLLM
from chat_llm import ChatLLM
import os

# craft a connection string and connect to the database
SERVER = os.getenv("DATABASE_SERVER")
DATABASE = os.getenv("DATABASE_NAME")
USERNAME = os.getenv("DATABASE_USERNAME")
PASSWORD = os.getenv("DATABASE_PASSWORD")
connectionString = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"

db = Database(connectionString)
db.connect()
db_schema = db.schema()

# create LLM instances
code_llm = CodeLLM(table_definitions=db_schema)
chat_llm = ChatLLM()


# create a class for queries
class QuestionRequest(BaseModel):
    question: str


#  create a FastAPI instance
app = FastAPI()

# allow CORS DONT DO THIS IN PRODUCTION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# handle question POST request
@app.post("/question")
async def question(question_request: QuestionRequest):
    print(f"Received question: {question_request.question}")

    code_llm_answer = code_llm.ask(question_request.question)
    print(f"Answer: {code_llm_answer}")

    sql_query = code_llm_answer.split("```sql")[1].split("```")[0]
    print(f"SQL Query: {sql_query}")

    sql_data = str(db.query(sql_query))
    print(f"SQL Data: {sql_data}")

    chat_llm_answer = chat_llm.ask(
        question=question_request.question, sql_query=sql_query, data=sql_data
    )

    print("Returning response...")
    return {
        "question": question_request.question,
        "code_llm_answer": code_llm_answer,
        "query": sql_query,
        "sql_data": sql_data,
        "chat_llm_answer": chat_llm_answer,
        "answer": chat_llm_answer,
        "result": "success",
    }


# handle disconnecting from database
@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")
    db.disconnect()
