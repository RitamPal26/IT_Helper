import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from admin_panel import database

app = FastAPI(title="Mock IT Admin Panel")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the main dashboard."""
    users = database.get_all_users()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"users": users}
    )

@app.get("/users", response_class=HTMLResponse)
async def manage_users(request: Request):
    """Render the user management page."""
    users = database.get_all_users()
    return templates.TemplateResponse(
        request=request,
        name="manage_users.html",
        context={"users": users}
    )

@app.post("/reset-password")
async def reset_password(email: str = Form(...), new_password: str = Form(...)):
    """Reset a user's password and redirect to the users page."""
    database.reset_password(email, new_password)
    return RedirectResponse(url="/users", status_code=303)

@app.post("/create-user")
async def create_user(email: str = Form(...), name: str = Form(...), password: str = Form(...)):
    """Create a new user and redirect to the users page."""
    database.create_user(email, name, password)
    return RedirectResponse(url="/users", status_code=303)
