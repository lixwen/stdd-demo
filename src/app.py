from fastapi import FastAPI

from src.routes.todos import router as todos_router

app = FastAPI(title="STDD Demo API", version="0.1.0")
app.include_router(todos_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
