# Imports
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcq_project.logger import logging
from src.mcq_project.utils import read_file, get_table_data, template_creation

# Imports from the LangChain library
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


# Load the environment variables
load_dotenv() # Takes environ values from .env file

# Load the API key
KEY = os.getenv("OPENAI_API_KEY")

# Call the OpenAI API
llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-3.5-turbo", temperature=0.3)

# The prompt template for the input and output, few-shot prompts
TEMPLATE, TEMPLATE_2 = template_creation()

# Create the prompt template
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

# Create the chain object, output of the first chain is the input of the second chain, which is "quiz" in this case
quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

# Create the prompt template for the second chain, subject and quiz are the input variables
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE_2)

# Create the second chain object, review is the output of the second chain
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Connect the chains in a sequence chain
generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain, review_chain], 
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"], 
    verbose=True
)