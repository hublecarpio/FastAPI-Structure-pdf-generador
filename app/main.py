from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.routes import auth, templates, render, apikeys, me, web, images, pdf_convert
from app.core.database import engine, Base
from app.models import user, template, apikey, renderlog


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
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

app.include_router(auth.router, prefix="/api")
app.include_router(me.router, prefix="/api")
app.include_router(apikeys.router, prefix="/api")
app.include_router(templates.router, prefix="/api")
app.include_router(render.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(pdf_convert.router, prefix="/api")
app.include_router(web.router)


@app.get("/health")
async def health():
    return {"status": "healthy"}
