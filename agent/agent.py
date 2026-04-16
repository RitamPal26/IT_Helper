import os
import asyncio
import logging
import discord
from dotenv import load_dotenv
from browser_use_sdk.v3 import AsyncBrowserUse

logging.basicConfig(level=logging.INFO, format="%(message)s")
load_dotenv()

class DiscordITAgent:
    """An autonomous agent handling IT requests with secure auth pausing."""

    def __init__(self):
        self.client = AsyncBrowserUse()
        self.pending_tasks = {}

    async def initiate_login(self, user_id: int, user_request: str) -> str:
        """Step 1: Create session, navigate to login, and return Live URL for human."""
        session = await self.client.sessions.create()
        
        self.pending_tasks[user_id] = {
            "session_id": session.id,
            "task": user_request
        }

        prompt = "Go to https://www.notion.so/login, type 'rp4528@srmist.edu.in' into the email field, click continue, and then stop."
        
        logging.info("[SYSTEM] Navigating to Notion login...")
        run = self.client.run(prompt, session_id=session.id)
        
        async for _ in run:
            pass 

        return session.live_url

    async def execute_pending_task(self, user_id: int) -> str:
        """Step 2: Resume the session and execute the actual task."""
        if user_id not in self.pending_tasks:
            return "No pending authentication found. Start a new task with '!it'."

        session_id = self.pending_tasks[user_id]["session_id"]
        task = self.pending_tasks[user_id]["task"]

        prompt = (
            "You are an IT agent. The human has successfully logged in, and you are on the Notion dashboard.\n"
            f"Fulfill this user request exactly: '{task}'\n"
            "CRITICAL NAVIGATION RULES:\n"
            "1. Close any onboarding popups or modals first.\n"
            "2. Click '+ Add new' under the 'Private' sidebar section.\n"
            "3. Click the 'Untitled' page title area and type the requested title.\n"
            "4. IMMEDIATELY press the 'Escape' key or click an empty space to dismiss any floating toolbars.\n"
            "5. Click below the title to add the requested heading.\n"
            "CRITICAL: Keep your final response to a single, short sentence confirming success."
        )

        logging.info(f"\n[SYSTEM] Resuming task: '{task}'")
        run = self.client.run(prompt, session_id=session_id)
        
        ignore_logs = ["Fetch", "Running JavaScript", "Running Python code", "We're already on"]
        async for msg in run:
            if msg.summary and msg.role != "tool":
                if not any(ignored in msg.summary for ignored in ignore_logs):
                    print(f"[{msg.role.upper()}] {msg.summary}")

        result = run.result.output if run.result else "Task completed, but no output returned."
        
        await self.client.sessions.stop(session_id)
        del self.pending_tasks[user_id]
        
        return result

intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)
it_agent = DiscordITAgent()

@discord_client.event
async def on_ready():
    print(f"Logged in to Discord as {discord_client.user}!")
    print("Ready to receive '!it' commands.")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith('!it '):
        user_request = message.content[4:]
        await message.channel.send(f"**Acknowledged:** Getting Notion ready for: *{user_request}*...")
        
        live_url = await it_agent.initiate_login(message.author.id, user_request)
        
        auth_msg = (
            f"**Authentication Required:** Notion requires a secure OTP.\n"
            f"1. Click this secure live view link: {live_url}\n"
            f"2. Check your email, enter the OTP, and wait for the Notion dashboard to load.\n"
            f"3. Return to Discord and type **`!continue`**."
        )
        await message.channel.send(auth_msg)

    elif message.content == '!continue':
        await message.channel.send("**Resuming:** Taking control of the browser to execute the task...")
        result = await it_agent.execute_pending_task(message.author.id)
        await message.channel.send(f"**Update:** {result}")

if __name__ == "__main__":
    discord_token = os.getenv("DISCORD_TOKEN")
    if not discord_token:
        print("Error: DISCORD_TOKEN not found in .env")
    else:
        discord_client.run(discord_token)