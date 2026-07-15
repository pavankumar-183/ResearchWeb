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
INSTRUCTIONS = """
You are a senior research writer.

Given the user's query and the search summaries,
produce a detailed report.

Return ONLY valid JSON.

Format:

{
    "short_summary":"...",
    "markdown_report":"...",
    "follow_up_questions":[
        "...",
        "..."
    ]
}

Do not return markdown.
Do not use code fences.
Return only JSON.
"""

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model=model,
    
)