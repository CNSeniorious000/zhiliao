from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from app.models import Message
from app.storage import Storage, get_next_id

router = APIRouter(prefix="/records", tags=["Record"])

store = Storage("records", dict)


@router.get("", response_model=list[str])
async def get_all_record_keys():
    return list(await store)


@router.get(
    "/{record_id}", response_model=list[Message], response_model_exclude_unset=True
)
async def get_a_record(record_id: str):
    try:
        return await store[record_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Record not found")


@router.post("", status_code=201, response_class=PlainTextResponse)
async def add_a_record(data: list[Message]):
    record_id = get_next_id(await store)
    await store.update({record_id: [i.dict(exclude_unset=True) for i in data]})
    return record_id


@router.put("/{record_id}", status_code=204)
async def update_a_record(record_id: str, data: list[Message]):
    try:
        await store.update({record_id: [i.dict(exclude_unset=True) for i in data]})
    except KeyError:
        raise HTTPException(status_code=404, detail="Record not found")


@router.delete("/{record_id}", status_code=204)
async def delete_a_record(record_id: str):
    try:
        await store.pop(record_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Record not found")
