import os
import resend
from typing import Dict
from agents import Agent , function_tool,OpenAIChatCompletionsModel
from openai import AsyncOpenAI

resend.api_key = os.getenv("RESEND_API_KEY")

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-oss-120b",
    openai_client=client,
)

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body."""

    response = resend.Emails.send(
        {
            "from": "naidupavan183@gmail.com",  
            "to": ["pavannaidu0219@gmail.com"],  
            "subject": subject,
            "html": html_body,
        }
    )

    print("Email response:", response)

    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=model,
)