# from dotenv import load_dotenv
# load_dotenv()

# from langchain_mistralai import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# #1. prompt template
# prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in simple words"
# )

# #2. Model
# model=ChatMistralAI(model="mistral-small-2506")

# #3. Output Parser
# parser=StrOutputParser()

# #step-by-step manual flow

# #Format the prompt 
# formatted_prompt=prompt.format_messages(topic="Machine Learning")

# #call the model manually
# response=model.invoke(formatted_prompt)

# #Parse the output manually
# final_output=parser.parse(response.content)

# print(final_output)

############################  Using Runnables ##################################
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words"
)

model = ChatMistralAI(model="mistral-small-2506")

parser=StrOutputParser()

chain = prompt | model | parser

result = chain.invoke("Machine Learning")
print(result)


