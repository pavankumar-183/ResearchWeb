import asyncio
import json

from agents import Runner
from search_agents import search_agent
from planner_agents import planner_agent, WebSearchItem, WebSearchPlan
from write_agent import writer_agent, ReportData
from email_Agent import email_agent


class ResearchManager:

    @staticmethod
    async def plan_searches(query: str) -> WebSearchPlan:
        print("Planning searches...")

        result = await Runner.run(
            planner_agent,
            f"Query: {query}"
        )

        data = json.loads(result.final_output)
        search_plan = WebSearchPlan(**data)

        print(f"Will perform {len(search_plan.searches)} searches")

        return search_plan

    @staticmethod
    async def search(item: WebSearchItem) -> str | None:
        """Perform one web search."""

        prompt = (
            f"Search term: {item.query}\n"
            f"Reason for searching: {item.reason}"
        )

        try:
            result = await Runner.run(
                search_agent,
                prompt
            )

            return str(result.final_output)

        except Exception as e:
            print(f"Search failed: {e}")
            return None

    @staticmethod
    async def perform_searches(search_plan: WebSearchPlan) -> list[str]:
        print("Searching...")

        tasks = [
            asyncio.create_task(
                ResearchManager.search(item)
            )
            for item in search_plan.searches
        ]

        results = []

        completed = 0

        for task in asyncio.as_completed(tasks):

            result = await task

            if result is not None:
                results.append(result)

            completed += 1
            print(f"{completed}/{len(tasks)} completed")

        print("Finished searching")

        return results

    @staticmethod
    async def write_report(
        query: str,
        search_results: list[str]
    ) -> ReportData:

        print("Writing report...")

        prompt = f"""
Original query:

{query}

Search Results:

{search_results}
"""

        result = await Runner.run(
            writer_agent,
            prompt
        )

        data = json.loads(result.final_output)

        report = ReportData(**data)

        print("Finished report")

        return report

    @staticmethod
    async def email_report(report: ReportData):

        print("Sending email...")

        await Runner.run(
            email_agent,
            report.markdown_report
        )

        print("Email sent.")