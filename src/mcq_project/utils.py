import os
import PyPDF2
import json
import traceback

def read_file(file_path):
    """
    Read the file and return the text
    """
    if file_path.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            raise Exception(f"Error in reading the PDF file: {e}")
        
    elif file_path.name.endswith(".txt"):
        return file_path.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format. Please provide a PDF or a text file.")
    
def get_table_data(quiz_str):
    """
    Get the table data from the text
    """
    try:
        # Convert the quiz string to a dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " | ".join(
            [
                f"{option}: {option_value}"
                for option, option_value in value["options"].items()
            ]
            )
        
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
    
def template_creation():
    """
    Create the template for the quiz generation
    """
    TEMPLATE= """
        Text:{text}
        You are an expert MCQ maker. Given the above text, it is your job to \
        create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
        Make sure the questions are not repeated and check all the questions to be conforming the text as well.
        Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
        Ensure to make {number} MCQs
        ### RESPONSE_JSON
        {response_json}
    
    """

    TEMPLATE_2="""
        You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
        You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
        if the quiz is not at per with the cognitive and analytical abilities of the students,\
        update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
        Quiz_MCQs:
        {quiz}

        Check from an expert English Writer of the above quiz:
        """
    
    return TEMPLATE, TEMPLATE_2