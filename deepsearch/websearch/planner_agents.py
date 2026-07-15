from pydantic import BaseModel , Field
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

load_dotenv(override=True)

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-oss-120b",
    openai_client=client,
)

How_Many_Searches = 4

INSTRUCTIONS = f"""
You are an expert research planner.

Given a user's query, generate exactly {How_Many_Searches} web search queries.

Return ONLY valid JSON in the following format:

{{
  "searches": [
    {{
      "reason": "Why this search is useful",
      "query": "The search query"
    }}
  ]
}}

Rules:
- Return exactly {How_Many_Searches} search items.
- Return only JSON.
- Do not include markdown.
- Do not include code fences.
- Do not include explanations or extra text.
"""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Why this search is important")
    query: str = Field(description="Search query")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="List of web searches"
    )

planner_agent = Agent(
    name="Planner Agent",
    instructions=INSTRUCTIONS,
    model=model,
 
    
)