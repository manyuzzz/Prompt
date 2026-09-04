import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config.settings import settings
from app.db.database import init_db
from app.routers import auth, chat, resume, roadmap, interview, coding, aptitude, companies, progress


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    await init_db()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info("Server ready!")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-powered placement preparation platform for engineering students",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(interview.router)
app.include_router(coding.router)
app.include_router(aptitude.router)
app.include_router(companies.router)
app.include_router(progress.router)

upload_dir = settings.UPLOAD_DIR
os.makedirs(upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "version": settings.VERSION, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
