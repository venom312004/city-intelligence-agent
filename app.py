"""
City Intelligence System - Streamlit UI
-----------------------------------------
LangChain + Mistral agent with weather & news tools, with a
human-in-the-loop approval step before every tool call.

Important: `input()` cannot work in Streamlit (no stdin, and the whole
script re-runs on every interaction). So the approval flow uses
LangGraph's `interrupt()` + a checkpointer, which is the correct way
to pause a create_agent() run and resume it after a user clicks a
button in the UI.
"""

import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from tavily import TavilyClient

load_dotenv()

# ─────────────────────────────────────────
# Pull secrets from Streamlit Cloud if not already in env (local .env still works)
# ─────────────────────────────────────────
for key in ["MISTRAL_API_KEY", "OPENWEATHER_API_KEY", "TAVILY_API_KEY"]:
    if not os.getenv(key):
        try:
            os.environ[key] = st.secrets[key]
        except Exception:
            pass

st.set_page_config(
    page_title="City Intelligence System",
    page_icon="🌆",
    layout="centered",
)

# ─────────────────────────────────────────
# TOOLS (same logic as your script)
# ─────────────────────────────────────────
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"Weather in {city}: {desc}, {temp}°C"


@tool
def get_news(city: str) -> str:
    """Get latest news about the city."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=f"{city} news today latest headlines",
        search_depth="advanced",
        max_results=5,
    )
    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"

    news_list = []
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")
        news_list.append(f"- {title}\n  {url}\n  {snippet[:100]}...")

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# ─────────────────────────────────────────
# MIDDLEWARE: interrupt() instead of input()
# ─────────────────────────────────────────
@wrap_tool_call
def human_approval(request, handler):
    """Pause the agent and hand control back to the Streamlit UI."""
    decision = interrupt(
        {
            "tool_name": request.tool_call["name"],
            "tool_args": request.tool_call["args"],
        }
    )
    if decision != "approve":
        return ToolMessage(
            content="Tool call denied by user",
            tool_call_id=request.tool_call["id"],
        )
    return handler(request)


# ─────────────────────────────────────────
# AGENT (cached once per server process; isolated per user via thread_id)
# ─────────────────────────────────────────
@st.cache_resource
def get_agent():
    llm = ChatMistralAI(model="mistral-small-2506")
    checkpointer = InMemorySaver()
    return create_agent(
        llm,
        tools=[get_news, get_weather],
        system_prompt="You are a helpful city assistant.",
        middleware=[human_approval],
        checkpointer=checkpointer,
    )


agent = get_agent()

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []  # chat bubbles shown in UI
if "pending_interrupts" not in st.session_state:
    st.session_state.pending_interrupts = []  # list of Interrupt objects
if "interrupt_decisions" not in st.session_state:
    st.session_state.interrupt_decisions = {}  # {interrupt_id: "approve"/"deny"}
if "interrupt_cursor" not in st.session_state:
    st.session_state.interrupt_cursor = 0  # which pending interrupt we're on
if "require_approval" not in st.session_state:
    st.session_state.require_approval = True

config = {"configurable": {"thread_id": st.session_state.thread_id}}


def run_until_response(result):
    """Drive the agent forward. If approval is required, stop and let the
    UI show approval cards. If approval is turned off, auto-approve every
    pending tool call and keep going until a final reply comes back."""
    while result.get("__interrupt__"):
        interrupts = result["__interrupt__"]
        if st.session_state.require_approval:
            st.session_state.pending_interrupts = list(interrupts)
            st.session_state.interrupt_decisions = {}
            st.session_state.interrupt_cursor = 0
            return
        decisions = {i.id: "approve" for i in interrupts}
        result = agent.invoke(Command(resume=decisions), config=config)

    reply = result["messages"][-1].content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.pending_interrupts = []
    st.session_state.interrupt_decisions = {}
    st.session_state.interrupt_cursor = 0


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.header("🌆 City Intelligence")
    st.caption("Weather + News agent, powered by Mistral AI")
    st.divider()
    st.toggle(
        "🔒 Require approval for tool calls",
        key="require_approval",
        help="When off, the agent auto-approves its own tool calls (weather/news lookups run instantly).",
    )
    st.divider()
    st.markdown("**Try asking:**")
    for example in [
        "Weather in Delhi",
        "Latest news in Bengaluru",
        "Weather and news in Mumbai",
    ]:
        if st.button(example, use_container_width=True, key=f"ex_{example}"):
            st.session_state["_prefill"] = example
    st.divider()
    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.pending_interrupts = []
        st.session_state.interrupt_decisions = {}
        st.session_state.interrupt_cursor = 0
        st.rerun()

# ─────────────────────────────────────────
# MAIN CHAT UI
# ─────────────────────────────────────────
st.title("🌆 City Intelligence System")
if st.session_state.require_approval:
    st.caption("Every tool call needs your approval before it runs — human-in-the-loop.")
else:
    st.caption("Auto-approve is ON — the agent runs tool calls instantly.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Pending approval card(s) — agent may request several tools at once,
# so we walk through them one at a time and resume all together at the end.
pending = st.session_state.pending_interrupts
cursor = st.session_state.interrupt_cursor

if pending:
    if cursor < len(pending):
        current = pending[cursor]
        data = current.value
        with st.chat_message("assistant"):
            if len(pending) > 1:
                st.caption(f"Approval {cursor + 1} of {len(pending)}")
            st.warning(
                f"🔧 Agent wants to call **`{data['tool_name']}`** "
                f"with args `{data['tool_args']}`. Approve?"
            )
            col1, col2 = st.columns(2)
            approve = col1.button("✅ Approve", use_container_width=True, key=f"approve_{cursor}")
            deny = col2.button("❌ Deny", use_container_width=True, key=f"deny_{cursor}")

        if approve or deny:
            st.session_state.interrupt_decisions[current.id] = (
                "approve" if approve else "deny"
            )
            st.session_state.interrupt_cursor += 1
            st.rerun()
    else:
        # All pending interrupts have a decision — resume the agent once
        with st.spinner("Resuming agent..."):
            result = agent.invoke(
                Command(resume=st.session_state.interrupt_decisions), config=config
            )
        run_until_response(result)
        st.rerun()

# Chat input (disabled while an approval is pending)
prefill = st.session_state.pop("_prefill", None)
prompt = st.chat_input(
    "Ask about weather or news in a city...",
    disabled=bool(pending),
)
prompt = prompt or prefill

if prompt and not pending:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        result = agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}, config=config
        )
    run_until_response(result)
    st.rerun()