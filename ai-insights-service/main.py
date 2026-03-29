from fastapi import FastAPI
from dotenv import load_dotenv
from routers import insights

load_dotenv()

app = FastAPI(
    title="FinSight AI Insights Service",
    description="AI-powered financial insights using LangChain and Ollama",
    version="1.0.0"
)

app.include_router(insights.router)


@app.get("/health")
async def health_check():
    return {"status": "UP", "service": "ai-insights-service"}