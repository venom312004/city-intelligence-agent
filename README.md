# 🔗 LangChain Runnables & Agents

*A hands-on exploration of LangChain's core building blocks — from LCEL runnables to tool calling and autonomous agents.*

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL%20%7C%20Agents-1C3C3C.svg)](https://www.langchain.com/)
[![Mistral AI](https://img.shields.io/badge/LLM-Mistral%20AI-FF7000.svg)](https://mistral.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

🔴 **Live Demo:** https://city-intelligence-agent-pranjal-pandey-2003.streamlit.app/

---

## 📖 Overview

This repo is a practical reference for how LangChain composes prompts, models, parsers, and tools into pipelines and agentic workflows — built while learning LangChain fundamentals from the ground up, using **Mistral AI** as the LLM backend.

## 📂 Project Structure

| File | Concept Covered |
|---|---|
| `sequence_runnable.py` | Basic LCEL chain — `prompt \| model \| parser` — the core sequential runnable pattern |
| `runnable_passthrough.py` | `RunnablePassthrough` for forwarding inputs unchanged through a chain |
| `parallel_runnables.py` | `RunnableParallel` — running multiple chains concurrently and merging outputs |
| `custom_tool.py` | Defining custom tools with the `@tool` decorator for agent use |
| `tool_calling.py` | Binding tools to a model and handling tool-call responses |
| `Agents.py` | Building agents with `create_agent` and reasoning over tool outputs |
| `auto_agents.py` | Autonomous agent execution without manual intervention |
| `news_summarizer.py` | Applied mini-project — fetching and summarizing news using an LLM chain |
| `app.py` | Entry point / demo runner tying the concepts together |
| `requirements.txt` | Project dependencies |

## ✨ Key Concepts Demonstrated

- **LCEL (LangChain Expression Language)** — declarative chain composition with `|`
- **Runnables** — `RunnableSequence`, `RunnableParallel`, `RunnablePassthrough`
- **Tool Calling** — custom tools bound to LLMs for structured actions
- **Agents** — reasoning loops that decide which tools to call and when

## 🛠️ Tech Stack

- **LangChain** (LCEL, Runnables, Agents, Tools)
- **Mistral AI** (`langchain-mistralai`) as the LLM provider
- **Python 3.11**

## 🚀 Setup

```bash
git clone https://github.com/venom312004/langchain-runnables-agents.git
cd langchain-runnables-agents

# create and activate a virtual environment
uv venv
.venv\Scripts\activate   # Windows PowerShell

# install dependencies
uv pip install -r requirements.txt
```

Create a `.env` file in the root with your API key:

```
MISTRAL_API_KEY=your_key_here
```

> ⚠️ `.env` is git-ignored — never commit real API keys.

## ▶️ Running

Each script is standalone — run any file directly to see that concept in action:

```bash
python sequence_runnable.py
python Agents.py
```

## 🎯 Why This Repo

Built as part of my path toward mastering **GenAI and agentic AI systems** — connecting core LangChain primitives to real, applied workflows before moving on to production-grade multi-agent projects.

## 👤 Author

**Pranjal Pandey**
B.Tech, Data Science & AI
[GitHub](https://github.com/venom312004) · [LinkedIn](#)

---

⭐ If this helped you understand LangChain runnables or agents, consider giving it a star!
