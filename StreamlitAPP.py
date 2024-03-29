import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_project.utils import read_file, get_table_data, template_creation
import streamlit as st

from langchain.callbacks import get_openai_callback
from src.mcq_project.MCQGenerator import generate_evaluate_chain
from src.mcq_project.logger import logging

# Load the response JSON
with open(r"C:\Users\caner\Desktop\MCQ_Project\Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

# Create the title of the web app
st.title(" Multiple Choice Quiz (MCQ) Generation and Evaluation with LangChain ⛓️⛓️")

# Create a form using st.form
with st.form(key="user_inputs"):
    # Create a file uploader
    uploaded_file = st.file_uploader("Upload a PDF or txt file", type=["pdf", "txt"])

    # Create input fields
    # response_json = st.text_area("Response JSON", json.dumps(RESPONSE_JSON, indent=4))

    # Create a number input for the number of questions
    number = st.number_input("Number of MCQ's", min_value=3, max_value=50)

    # Create a text area for the subject
    subject = st.text_input("Write the subject here...", max_chars=20)

    # Create a text area for the tone
    tone = st.text_input("Tone or complexity of the questions...", max_chars=20, placeholder="Simple, Intermediate, Complex etc.")

    # Create a submit button
    submit_button = st.form_submit_button(label="Generate MCQs")

    # If the submit button is clicked and all fields have input

    if submit_button and uploaded_file is not None and number and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                # Read the file
                text = read_file(uploaded_file)

                # Generate the quiz also count tokens and cost of the API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text, 
                        "number": number, 
                        "subject": subject, 
                        "tone": tone, 
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
                # st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"Error in generating the MCQs: {e}")
            else:
                # Print the billing information
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")

                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        # Get the quiz data
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index += 1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                            st.success("MCQs generated successfully.")
                        else:
                            st.error("Error in generating the MCQs.")
                else:
                    st.write(response)
