#First step - loading all the libraries
from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_cohere import ChatCohere
from langchain.tools import tool
from langchain_core.messages import HumanMessage,ToolMessage
from tavily import TavilyClient
from rich import print


# ─────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    print("DEBUG:", data)

    if response.status_code != 200:
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    return f"Weather in {city}: {desc}, {temp}°C"


@tool
def get_news(city: str) -> str:
    """Get latest news about the city."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []
    for r in results:
        title   = r.get("title", "No title")
        url     = r.get("url", "")
        snippet = r.get("content", "")
        news_list.append(f"- {title}\n  {url}\n  {snippet[:100]}...")

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# ─────────────────────────────────────────
# LLM SETUP
# ─────────────────────────────────────────

llm = ChatCohere(model="command-a-03-2025", temperature=0, max_retries=1, timeout=30)

# ✅ Renamed from 'tool' to 'tools_map' — 'tool' was overwriting the @tool decorator import
tools_map = {
    "get_news":    get_news,
    "get_weather": get_weather,
}

llm_with_tools = llm.bind_tools([get_news, get_weather])


# ─────────────────────────────────────────
# AGENT LOOP
# ─────────────────────────────────────────

messages = []

print("City Intelligence System")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    # Inner loop — keeps running until LLM gives a final answer
    while True:
        result = llm_with_tools.invoke(messages)
        messages.append(result)

        if result.tool_calls:
            tool_denied = False

            for tool_call in result.tool_calls:
                tool_name = tool_call['name']

                # Human-in-the-loop confirmation
                confirm = input(f"\nAgent wants to call '{tool_name}'. Approve? (yes/no): ").strip().lower()

                if confirm == "no":
                    print(f"[Denied] '{tool_name}' was not executed. Cannot fetch latest info.\n")
                    tool_denied = True
                    break

                # ✅ Execute the tool
                tool_result = tools_map[tool_name].invoke(tool_call)
                messages.append(ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call['id']
                ))

            if tool_denied:
                break  # ✅ Exit inner loop cleanly on denial

            continue  # Loop again so LLM can process tool results

        else:
            # No more tool calls — final LLM response
            print(f"\nAssistant: {result.content}\n")
            break  # ✅ Exit inner loop, wait for next user input


# Flow:
# User Input → LLM (decides tool) → Human confirms → Tool executes
#           → ToolMessage added → LLM loops → Final Answer