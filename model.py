from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_groq import ChatGroq

# Instantiate ChatGroq
chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")
system = "You are a Data Analyst"


def generate_overview(submission_details: list):

    prompt = ChatPromptTemplate.from_template("Generate an introduction for the student only consider the roll_no and the semester. Details are below: {details}")

    chain = prompt | chat
    result = chain.invoke({"details":submission_details})
    
    return result.content

def generate_code_recommendations(submission_details: list):

    prompt = ChatPromptTemplate.from_template("Analyze the code and provide tips focusing on areas like coding practices, problem-solving approaches, and language usage based on the overall coding style of the student.Consider only the submission field. Use simple and easy language. Short and sweet sentences. Details are below: {details}")

    chain = prompt | chat
    result = chain.invoke({"details":submission_details})
    
    return result.content

def generate_common_observation(submission_details: list):

    prompt = ChatPromptTemplate.from_template("Analyze student details and note within the common observations. Use simple and easy language. Short and sweet sentences. Details are below: {details}")

    chain = prompt | chat
    result = chain.invoke({"details":submission_details})
    
    return result.content

def generate_strength_and_weakness(submission_details: list):

    prompt = ChatPromptTemplate.from_template("Analyze student details, identify and note  the common strengths and weaknesses of the student.Use simple and easy language. Short and sweet sentences. Details are below: {details}")

    chain = prompt | chat
    result = chain.invoke({"details":submission_details})
    
    return result.content



def format_output(overview_content, code_recommendations_content, general_observations_content,strength_and_weakness):
    output_template = f"""
    <div class="container">
      <h2>Overview</h2>
      {overview_content}
      
      <h2>Code Recommendations</h2>
      {code_recommendations_content}
      
      <h2>General Observations</h2>
      {general_observations_content}
      
      <h2>Strength and Weakness</h2>
      {strength_and_weakness}
    </div>
    """
    return output_template
