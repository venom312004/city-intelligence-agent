# 🌆 City Intelligence System

**Agentic City Assistant — Weather · News · Human-in-the-Loop Tool Approval**

City Intelligence System is an agentic AI assistant that answers questions about any city's current weather and latest news. Built on LangGraph, it pauses before every tool call and asks for human approval — giving users full visibility and control over what the agent does before it acts.

---

## 🔗 Links

- **Live App:** [city-intelligence-agent.streamlit.app](https://city-intelligence-agent-pranjal-pandey-2003.streamlit.app/)

---

## 📌 Description

This project demonstrates a production-style **human-in-the-loop (HITL) agentic workflow** using LangGraph's `interrupt()` and checkpointer system — the correct way to pause a `create_agent()` run mid-execution inside a stateless, re-running Streamlit app (where a plain Python `input()` simply cannot work).

Ask a question like *"weather and news in Mumbai"*, and the agent decides which tools to call (`get_weather`, `get_news`), then **stops and shows an approval card** for each tool call before executing it. Approve or deny each one individually, and the agent resumes exactly where it left off — powered by Cohere as the reasoning engine.

---

## ✨ Features

- 🌤️ **Live Weather Lookup** — real-time conditions for any city via OpenWeatherMap
- 📰 **Latest News Search** — current headlines and summaries via Tavily Search
- 🛑 **Human-in-the-Loop Approval** — every tool call pauses for explicit user approval/denial before running
- 🔀 **Auto-Approve Toggle** — switch off approval mode for instant, uninterrupted responses
- 🧵 **Per-Session Memory** — isolated conversation threads via LangGraph's checkpointer
- 🗨️ **Multi-Tool Requests** — handles compound queries (e.g. "weather and news") by walking through each pending approval in sequence
- 🎨 **Clean Streamlit Chat UI** with sidebar quick-prompts and new-conversation reset

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (chat UI) |
| Agent Orchestration | LangGraph (`create_agent`, `interrupt()`, `Command`) |
| LLM Provider | Cohere (`langchain-cohere`, `command-a-03-2025`) |
| Middleware | Custom `wrap_tool_call` for HITL approval |
| State Management | LangGraph `InMemorySaver` checkpointer |
| Weather Data | OpenWeatherMap API |
| News Data | Tavily Search API |
| Deployment | Streamlit Community Cloud |

---

## 🚀 Getting Started

### Prerequisites
- Python ≥ 3.11
- Cohere API key
- OpenWeatherMap API key
- Tavily API key

### Installation

```bash
git clone https://github.com/venom312004/city-intelligence-agent.git
cd city-intelligence-agent

# create and activate a virtual environment
uv venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # macOS/Linux

# install dependencies
uv pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run Locally

```bash
streamlit run app.py
```

---

## 🧠 How the Human-in-the-Loop Flow Works

1. User asks a question (e.g. *"weather in Delhi"*)
2. The agent decides to call `get_weather`, and LangGraph's `interrupt()` pauses execution
3. Streamlit renders an **approval card** showing the tool name and arguments
4. User clicks **✅ Approve** or **❌ Deny**
5. The agent **resumes** from the exact interruption point via `Command(resume=...)` — no state is lost
6. If multiple tools are requested at once, the UI walks through each approval one at a time before resuming

This pattern solves a real constraint: Streamlit has no persistent stdin and re-runs the whole script on every interaction, so a naive `input()`-based approval loop is impossible. `interrupt()` + a checkpointer is the correct fix.

---

## 📁 Project Structure

```
city-intelligence-agent/
├── app.py                  # Streamlit UI, agent setup, HITL approval flow
├── requirements.txt
└── .gitignore
```

---

## ⚠️ Known Limitations

- Uses an **in-memory checkpointer**, so conversation state resets if the app restarts or reboots.
- Weather and news lookups depend on external free-tier APIs (OpenWeatherMap, Tavily) — rate limits may apply.
- Free-tier cloud hosting may briefly delay responses during cold starts.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [LangGraph](https://www.langchain.com/langgraph)
- [LangChain](https://www.langchain.com/)
- [Cohere](https://cohere.com/)
- [OpenWeatherMap](https://openweathermap.org/)
- [Tavily](https://tavily.com/)
- [Streamlit](https://streamlit.io/)