import os
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

from .rag.rag import search_documents
from .tools import github_info, users_info


load_dotenv()


# ---------------- LLM ----------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# ---------------- TOOLS ----------------

tools = [github_info, users_info]
llm_with_tools = llm.bind_tools(tools)


# ---------------- STATE ----------------

class AURAState(TypedDict):
    message: str
    route: str
    response: str
    tool_result: str


# ---------------- ROUTER ----------------

router_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are AURA's routing system.

Classify the user's request into exactly ONE category:

general
research
coding
tool

Rules:
- coding = programming, debugging, code or technical implementation
- research = factual research, document questions or knowledge retrieval
- tool = request requiring an external API or tool
- general = normal conversation and general questions

Return ONLY one word:
general, research, coding, or tool."""
    ),
    ("human", "{message}")
])


def router_node(state: AURAState):
    result = llm.invoke(
        router_prompt.invoke({
            "message": state["message"]
        })
    )

    route = result.content

    # Handle LangChain content-list format
    if isinstance(route, list):
        route = "".join(
            item.get("text", "")
            for item in route
            if isinstance(item, dict)
        )

    route = str(route).strip().lower()

    if route not in ["general", "research", "coding", "tool"]:
        route = "general"

    return {
        "route": route
    }


# ---------------- GENERAL AGENT ----------------

def general_agent(state: AURAState):
    result = llm.invoke(
        f"""You are AURA's General Agent.

Answer the user's question accurately, clearly and naturally.

User:
{state["message"]}
"""
    )

    return {
        "response": extract_text(result.content)
    }


# ---------------- RESEARCH AGENT + RAG ----------------

def research_agent(state: AURAState):
    documents = search_documents(state["message"])

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    result = llm.invoke(
        f"""You are AURA's Research Agent.

Answer the user's question using the provided document context.

Rules:
- Use the context as the primary source.
- Do not invent information.
- If the answer is not available in the context, clearly say that it was not found in the provided document.
- Give a clear and concise answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{state["message"]}
"""
    )

    return {
        "response": extract_text(result.content)
    }


# ---------------- CODING AGENT ----------------

def coding_agent(state: AURAState):
    result = llm.invoke(
        f"""You are AURA's Coding Agent.

Help the user with programming and technical problems.

Rules:
- Give correct code.
- Explain the important part briefly.
- Use clear formatting.

User:
{state["message"]}
"""
    )

    return {
        "response": extract_text(result.content)
    }


# ---------------- TOOL AGENT ----------------

def tool_agent(state: AURAState):
    result = llm_with_tools.invoke(state["message"])

    if result.tool_calls:
        tool_call = result.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})

        if tool_name == "github_info":
            tool_result = github_info.invoke(tool_args)

        elif tool_name == "users_info":
            tool_result = users_info.invoke(tool_args)

        else:
            tool_result = "Unknown tool"

        return {
            "tool_result": str(tool_result),
            "response": str(tool_result)
        }

    return {
        "response": extract_text(result.content)
    }


# ---------------- TEXT HELPER ----------------

def extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("text"):
                text_parts.append(item["text"])

        return "".join(text_parts)

    return str(content)


# ---------------- ROUTING ----------------

def route_decision(
    state: AURAState
) -> Literal["general", "research", "coding", "tool"]:

    return state["route"]


# ---------------- GRAPH ----------------

graph_builder = StateGraph(AURAState)

graph_builder.add_node("router", router_node)
graph_builder.add_node("general", general_agent)
graph_builder.add_node("research", research_agent)
graph_builder.add_node("coding", coding_agent)
graph_builder.add_node("tool", tool_agent)

graph_builder.add_edge(START, "router")

graph_builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "general": "general",
        "research": "research",
        "coding": "coding",
        "tool": "tool"
    }
)

graph_builder.add_edge("general", END)
graph_builder.add_edge("research", END)
graph_builder.add_edge("coding", END)
graph_builder.add_edge("tool", END)


aura_graph = graph_builder.compile()