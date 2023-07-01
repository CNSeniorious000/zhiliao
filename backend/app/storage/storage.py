from asyncio import Lock
from pathlib import Path

from aiofiles import open
from orjson import OPT_APPEND_NEWLINE, OPT_INDENT_2, dumps, loads

ROOT = Path("./data")

ROOT.mkdir(parents=True, exist_ok=True)


class Storage:
    def __init__(self, name: str, fallback=None):
        self.name = name
        self.path = ROOT / f"{name}.json"
        self.lock = Lock()
        self.fallback = fallback or (lambda: None)

    async def get_data(self, *, lock=True):
        if self.path.exists():
            if lock:
                await self.lock.acquire()
            else:
                assert self.lock.locked()

            async with open(self.path, "rb") as f:
                json = await f.read()

            if lock:
                self.lock.release()

            return loads(json or "null") or self.fallback()

        else:
            return self.fallback()

    async def set_data(self, data, *, lock=True):
        json = dumps(
            list(data) if isinstance(data, set) else data,
            option=OPT_APPEND_NEWLINE | OPT_INDENT_2,
        )

        if lock:
            await self.lock.acquire()
        else:
            assert self.lock.locked()

        async with open(self.path, "wb") as f:
            await f.write(json)

        if lock:
            self.lock.release()

    def __repr__(self):
        return str(self.data)

    def __await__(self):
        return self.get_data().__await__()

    def __getitem__(self, key):
        async def work():
            return (await self.get_data())[key]

        return work()

    __getattr__ = __getitem__

    async def get(self, key, default=None):
        data = await self.get_data()
        if isinstance(data, dict):
            return data.get(key, default)
        raise TypeError(data)

    async def clear(self):
        async with self.lock:
            data = await self.get_data(lock=False)
            data.clear()
            await self.set_data(data, lock=False)

    async def update(self, values):
        async with self.lock:
            data = await self.get_data(lock=False)
            if isinstance(data, dict):
                assert isinstance(values, dict)
                return await self.set_data(data | values, lock=False)
            if isinstance(data, list):
                assert isinstance(values, set)
                return await self.set_data(set(data) | values, lock=False)
            raise TypeError(data)

    async def append(self, value):
        async with self.lock:
            data = await self.get_data(lock=False)
            if isinstance(data, list):
                data.append(value)
                return await self.set_data(data, lock=False)
            raise TypeError(data)

    async def extend(self, values):
        async with self.lock:
            data = await self.get_data(lock=False)
            if isinstance(data, list):
                data.extend(values)
                return await self.set_data(data, lock=False)
            raise TypeError(data)

    async def remove(self, value):
        async with self.lock:
            data = await self.get_data(lock=False)
            if isinstance(data, list):
                data.remove(value)
                return await self.set_data(data, lock=False)
            raise TypeError(data)

    async def discard(self, value):
        try:
            return await self.remove(value)
        except ValueError:
            pass

    async def pop(self, key=None):
        async with self.lock:
            data = await self.get_data(lock=False)
            if key is not None and isinstance(data, list | dict):
                value = data.pop(key)
                await self.set_data(data, lock=False)
                return value
            if key is None and isinstance(data, list):
                data = set(data)
                value = data.pop()
                await self.set_data(data)
                return value
            raise TypeError(data)

    async def add(self, value):
        async with self.lock:
            data = await self.get_data(lock=False)
            if isinstance(data, list):
                data = set(data)
                data.add(value)
                return await self.set_data(data, lock=False)
            raise TypeError(data)
