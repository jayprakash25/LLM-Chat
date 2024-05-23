from fastapi import FastAPI, Body
from pydantic import BaseModel
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging


load_dotenv()

app = FastAPI()


origins = [
    "http://localhost:3000",  # Replace with your frontend origin
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# get vectorized salaries data
loader = CSVLoader(file_path="data/salaries.csv")
docs = loader.load()

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(docs, embeddings)
  
    
def retrieve_info(query):
    similar_response = vectorstore.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

# creating conversation chain
llm = ChatOpenAI(temperature=0)

template = """
You are an expert in the field of machine learning and data analysis. I will share a prospect's query with you, and you will provide the best response based on the available salary and job data from 2020 to 2024, following these rules:

1. Your response should closely match the relevant data points from the past, including details like salary ranges, job titles, and industry trends.

2. If the query cannot be directly answered using the available data, try to provide insights and analysis that mimic the style and format of the existing data.

Below is the query I received from the prospect:
{message}

Here are the relevant data points from the salary and job dataset:
{best_practice}

Please write the best response to address the prospect's query:
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Retrieval augmented generation
def generate_response(message):
    logging.info("Starting to generate")
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    logging.info('Finished generating')
    return response


class Message(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Chatbot! Please use /ask/ endpoint to ask a question."}

@app.post("/ask/")
async def generate_response_endpoint(message: Message = Body(...)):
    result = generate_response(message.content)
    return {"response": result}