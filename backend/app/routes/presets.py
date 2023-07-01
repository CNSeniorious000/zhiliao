from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.models import Preset
from app.storage import Storage, get_next_id

router = APIRouter(prefix="/presets")

store = Storage("presets", dict)


@router.get("", response_model=dict[str, Preset])
async def get_all_presets():
    return await store


@router.post("", status_code=201, response_class=PlainTextResponse)
async def add_a_preset(data: Preset):
    preset_id = get_next_id(await store)
    await store.update({preset_id: data.dict()})
    return preset_id


@router.put("/{preset_id}", status_code=204)
async def update_a_preset(preset_id: str, data: Preset):
    try:
        await store.update({preset_id: data.dict()})
    except KeyError:
        raise HTTPException(status_code=404, detail="Preset not found")


@router.delete("/{preset_id}", status_code=204)
async def delete_a_preset(preset_id: str):
    try:
        await store.pop(preset_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Preset not found")
