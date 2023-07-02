from fastapi import FastAPI

from app import presets

app = FastAPI(title="zhiliao")


app.include_router(presets.router)
