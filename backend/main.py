from fastapi import FastAPI

from app import presets

app = FastAPI()


app.include_router(presets.router)
