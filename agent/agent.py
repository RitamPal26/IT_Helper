import asyncio
import logging
import os
from dotenv import load_dotenv
from browser_use_sdk.v3 import AsyncBrowserUse

logging.basicConfig(level=logging.INFO, format="%(message)s")
load_dotenv()

class ITSupportAgent:
    """An autonomous agent that executes IT requests via browser automation."""

    def __init__(self, base_url: str):
        self.client = AsyncBrowserUse()
        self.base_url = base_url

    def _build_prompt(self, natural_language_request: str) -> str:
        """Constructs a strict instruction set wrapping the dynamic user request (DRY principle)."""
        return (
            f"You are an IT support agent. Start at exactly: {self.base_url}\n"
            "1. Navigate using the UI links (do not guess URLs).\n"
            f"2. Fulfill this user request: '{natural_language_request}'\n"
            "CRITICAL: Keep your final response to a single, short sentence confirming success or explaining what went wrong."
        )

    async def execute_task(self, user_request: str) -> str:
        """Executes the task with basic edge-case handling for system failures."""
        prompt = self._build_prompt(user_request)
        logging.info(f"Task Started: '{user_request}'")
        logging.info("Sending to Cloud... (Waiting for completion)")

        try:
            result = await self.client.run(prompt)
            return result.output
        except Exception as e:
            logging.error(f"SYSTEM ERROR: Failed to execute task. Details: {str(e)}")
            return "Task failed due to a system error."

async def main():
    """Main execution block to run multiple tasks."""
    ngrok_url = os.getenv("NGROK_URL")
    
    if not ngrok_url:
        raise ValueError("NGROK_URL is missing from the .env file.")

    agent = ITSupportAgent(base_url=ngrok_url)

    req1 = "Reset the password for john@company.com to old_password_123"
    res1 = await agent.execute_task(req1)
    print(f"Result 1: {res1}\n")
    print("-" * 40 + "\n")

    req2 = "Create a new user. Name: Sarah Admin, Email: sarah@company.com, Temporary Password: welcome123"
    res2 = await agent.execute_task(req2)
    print(f"Result 2: {res2}\n")

if __name__ == "__main__":
    asyncio.run(main())