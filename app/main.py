# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from interface.api import health, onboarding, ask, recommend, metrics
from infrastructure.logging import logger

# Load environment variables
load_dotenv()

app = FastAPI(title="QLIQ AI Assistant")

# Register Routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(onboarding.router, prefix="/onboard", tags=["Onboarding"])
app.include_router(ask.router, prefix="/ask", tags=["Ask"])
app.include_router(recommend.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/")
def root():
    logger.info("QLIQ AI Assistant Root")
    return {"message": "QLIQ AI Assistant is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

