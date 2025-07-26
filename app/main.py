# app/main.py
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.logging import logger
from infrastructure.middleware.logging_middleware import SimpleLoggingMiddleware
from infrastructure.vector_db.chroma_client import build_all_collections
from interface.api import health, onboarding, ask, recommend, metrics, classifier_comparison

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(fastApi: FastAPI):
    build_all_collections()  # only once at startup
    yield


app = FastAPI(title="QLIQ AI Assistant", lifespan=lifespan)

# Add middleware
app.add_middleware(SimpleLoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Register Routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(onboarding.router, prefix="/onboard", tags=["Onboarding"])
app.include_router(ask.router, prefix="/ask", tags=["Ask"])
app.include_router(classifier_comparison.router, prefix="/classifier-compare", tags=["classifier-compare"])
app.include_router(recommend.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])


@app.get("/")
def root():
    logger.info("QLIQ AI Assistant Root")
    return {"message": "QLIQ AI Assistant is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
