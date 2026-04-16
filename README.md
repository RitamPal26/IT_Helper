# IT Helper: An AI Agent that helps you do boring work

IT Helper is a proof-of-concept system demonstrating how Artificial Intelligence can automate routine IT support tasks. It consists of two parts:

1. **Mock IT Admin Panel:** A lightweight, functional web application serving as a simulated corporate IT dashboard.
2. **Autonomous AI Agent:** An AI worker that takes natural-language requests (e.g., "Reset John's password") and physically navigates the web interface using browser automation to complete the task, exactly like a human IT professional would.

## Demo Video

https://www.loom.com/share/053a0b806bb14525880584d1469af0fa

## Tech Stack

- **AI Agent framework:** [Browser Use Cloud SDK](https://browser-use.com/)
- **Backend Web Server:** Python, FastAPI
- **Frontend UI:** HTML5, Jinja2 Templates

## How to Setup and Run Locally

### 1. Environment Setup

Clone the repository and set up a fresh Python virtual environment to isolate dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies

Install the required packages for both the web server and the AI agent.

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the root directory and add your Browser Use Cloud API key.

```text
BROWSER_USE_API_KEY=your_api_key_here
NGROK_URL=your_ngrok_url_here
```

### 4. Start the Mock IT Panel

Run the FastAPI application. It will default to port 8000.

```bash
uvicorn admin_panel.app:app --reload
```

### 5. Expose to the Cloud via ngrok

Because the AI agent runs in the cloud, it needs a public URL to access your local panel. Open a new terminal and run:

```bash
ngrok http 8000
```

_Copy the forwarding URL provided by ngrok (e.g., `https://your-url.ngrok-free.app`)._

### 6. Run the AI Agent

Open `agent/browser_agent.py` and update the `base_url` parameter with your new ngrok URL. Then, execute the agent:

```bash
python agent/browser_agent.py
```
