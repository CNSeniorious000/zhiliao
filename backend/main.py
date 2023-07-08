from fastapi import FastAPI

from app import presets, records

app = FastAPI(title="zhiliao")


app.include_router(presets.router)
app.include_router(records.router)
