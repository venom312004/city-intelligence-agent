from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from rich import print

#1 creating a tool
@tool
def get_text_length(text:str)->int:
    """Returns the number of character in a given text"""
    return len(text)

llm=ChatMistralAI(model="mistral-small-2506")

#2 Tool binding
llm_with_tool=llm.bind_tools([get_text_length])

tool={
    "get_text_length":get_text_length
}

# result=llm.invoke("hello")
# result2=llm_with_tool.invoke("hello")
# print(result.content)
# print(result)
# print()
# print()
# print(result2)

# result=llm.invoke("Returns the number of character in a given text:Hello,how are you")
# result2 = llm_with_tool.invoke("What is the length of the text :'Hello, how are you'?")
# print(result)
# print()
# print()
# print()
# print()
# print(result2)
# print(result2.tool_calls)
# print(result2.tool_calls[0])

# if result2.tool_calls:
#     tool_call=result2.tool_calls[0]
#     tool_name=tool_call['name']
#     tool_args=tool_call['args']
#     tool_result=get_text_length.invoke(tool_args)
#     print(f"Text length: {tool_result}")
    
# print(result2.tool_calls[0])
# print(get_text_length.invoke({'name': 'get_text_length', 'args': {'text': 'Hello, how are you'}, 'id': 'e8vjalcQ1', 'type': 'tool_call'}))
message=[]
prompt=input("You : ")
query=HumanMessage(prompt)
message.append(query)

result=llm_with_tool.invoke(message)
message.append(result)
# print(message)

if result.tool_calls:
    tool_name=result.tool_calls[0]['name']
    tool_message=tool[tool_name].invoke(result.tool_calls[0])
    message.append(tool_message)
    # print(message)

result=llm_with_tool.invoke(message)
print(result.content)
 
    