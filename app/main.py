from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, templates, render, apikeys, me, web

app = FastAPI(
    title="PDF Template Rendering API",
    description="API for managing HTML templates and rendering them as PDFs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web.router)
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(apikeys.router)
app.include_router(templates.router)
app.include_router(render.router)


@app.get("/health")
async def health():
    return {"status": "healthy"}
