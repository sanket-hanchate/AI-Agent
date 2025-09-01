import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Cohere 

# Load API key
load_dotenv()

# Initialize Cohere LLM (auto uses env var COHERE_API_KEY)
llm = Cohere(temperature=0.5, max_tokens=400)

# Prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are an expert planner. Given a topic, create a detailed, step-by-step planning report.

Topic: {topic}
Detailed Report:
"""
)

# Memory for tracking conversation
memory = ConversationBufferMemory(input_key="topic", memory_key="chat_history")

# Chain setup
planning_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

def run_planning_agent(topic):
    return planning_chain.run(topic)


