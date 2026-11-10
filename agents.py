from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , Scrape_url
from pydantic import BaseModel , ValidationError , validate_call
import os
from dotenv import load_dotenv
load_dotenv()

#model setup
llm = ChatGroq(model = "openai/gpt-oss-120b", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

#First agent search
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

#second agent read
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[Scrape_url]
    )

#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are an expert research writer. Write clear, structured and insightful report"),
    ("human", """write a detailed research report on the below. 
    
    Topic:{topic}
    
    Research Gathered: {research}

    Structure the report as: 
    -Introduction
    -Key findings (minimum 3 well-explained points
    -Conclusion
    -Sources (list all URL's found in the research)
    
    Be detailed, factual and professional."""),
])


writer_chain = writer_prompt | llm | StrOutputParser()


#critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a sharp and constructive research critic. Be honest and specific"), 
    ("human", """review the research report below and evaluate it strictly.
    
    Report: {report}
    
    Respond in the same format:
    Score: x/10
    
    Strengths: 
    -...
    -...

    Areas to Improve:
    -...
    -...

    One line verdict:
    ...
    """),
])


critic_chain = critic_prompt | llm | StrOutputParser()

