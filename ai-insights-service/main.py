from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import insights

load_dotenv()

app = FastAPI(
    title="FinSight AI Insights Service",
    description="AI-powered financial insights using LangChain and Ollama",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insights.router)

@app.get("/health")
async def health_check():
    return {"status": "UP", "service": "ai-insights-service"}