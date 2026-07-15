import os
from dotenv import load_dotenv
from ddgs import DDGS
from openai import AsyncOpenAI

from agents import (
    Agent,
    function_tool,
    OpenAIChatCompletionsModel,
    ModelSettings,
    set_tracing_disabled,
)

load_dotenv(override=True)
set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-oss-120b",
    openai_client=client,
)


@function_tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return the top results.
    """

    print(f"\nSearching the web for: {query}\n")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No search results found."

        formatted_results = []

        for i, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
Result {i}

Title:
{result.get("title", "N/A")}

URL:
{result.get("href", "N/A")}

Summary:
{result.get("body", "No summary available.")}
"""
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Web search failed: {str(e)}"


SEARCH_INSTRUCTIONS = """
You are an expert research assistant.

You have access to one tool:

web_search(query: str)

Rules:

1. Always call the web_search tool exactly once.
2. Pass the complete search request using ONLY the parameter:
   query
3. Never generate parameters such as:
   id
   cursor
   page
   offset
   limit
   index
   start
4. Wait for the tool response.
5. Produce a concise summary of the search results.
6. Keep the summary below 250 words.
7. Write only the summary.
8. Do not mention the tool.
9. Ignore advertisements and duplicate information.
10. Focus only on factual information.
"""


search_agent = Agent(
    name="Search Agent",
    instructions=SEARCH_INSTRUCTIONS,
    model=model,
    tools=[web_search],
    model_settings=ModelSettings(
        tool_choice="required",
        temperature=0.5,
    ),
)