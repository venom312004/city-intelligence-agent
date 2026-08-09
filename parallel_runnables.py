# from dotenv import load_dotenv
# load_dotenv()

# from langchain_mistralai import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableParallel


#components
# model=ChatMistralAI(model="mistral-small-2506")
# parser=StrOutputParser()

#Two different prompts
# short_prompt=ChatPromptTemplate.from_template(
#     "Explain {topic} in 1-2 lines"
# )

# detailed_prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in detail"
# )

# Input
# topic="Machine Learning"

# without runnables
# formatted_short=short_prompt.format_messages(topic=topic)
# response_short=model.invoke(formatted_short)
# str_out=parser.parse(response_short.content)

# formatted_detailed=detailed_prompt.format_messages(topic=topic)
# response_detailed=model.invoke(formatted_detailed)
# str_out=parser.parse(response_detailed.content)

#using parallel runnable
# parallel_runnables= RunnableParallel({
#    "short": short_prompt | model | parser,
#     "detailed":detailed_prompt | model | parser
# })

# result=parallel_runnables.invoke({"topic":"Machine Learning"})
# print(result)
# print(result['short'])
# print(result['detailed'])


############################# Runnable Lambda #########################################
#use case "in a case where topic is machine learning in short_prompt and deep learning in detailed_prompt so use this syntax"
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda

model=ChatMistralAI(model="mistral-small-2506")
parser=StrOutputParser()


short_prompt=ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines"
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in detail"
)
parallel_runnables= RunnableParallel({
   "short": RunnableLambda(lambda x:x['short'])|short_prompt | model | parser,
    "detailed":RunnableLambda(lambda  x:x['detailed']) |detailed_prompt | model | parser
})

result=parallel_runnables.invoke({'short':{'topic':"Machine Learning"},
                                  'detailed':{"topic":"Deep Learning"}})
print(result['short'])
print(result['detailed'])

