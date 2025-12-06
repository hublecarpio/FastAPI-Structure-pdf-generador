from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["web"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "current_user": None})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "current_user": None})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "current_user": {"email": ""}})


@router.get("/templates", response_class=HTMLResponse)
async def templates_page(request: Request):
    return templates.TemplateResponse("templates_list.html", {"request": request, "current_user": {"email": ""}})


@router.get("/templates/new", response_class=HTMLResponse)
async def new_template_page(request: Request):
    return templates.TemplateResponse("template_form.html", {"request": request, "current_user": {"email": ""}, "template": None})


@router.get("/templates/{template_id}/edit", response_class=HTMLResponse)
async def edit_template_page(request: Request, template_id: int):
    return templates.TemplateResponse("template_form.html", {"request": request, "current_user": {"email": ""}, "template": {"id": template_id}})


@router.get("/render", response_class=HTMLResponse)
async def render_page(request: Request):
    return templates.TemplateResponse("render.html", {"request": request, "current_user": {"email": ""}})


@router.get("/apikeys", response_class=HTMLResponse)
async def apikeys_page(request: Request):
    return templates.TemplateResponse("apikeys.html", {"request": request, "current_user": {"email": ""}})
