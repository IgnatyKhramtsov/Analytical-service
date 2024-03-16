from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI, status

from database import SessionDep
from device.schemas import DevDataCreate, DeviceStatistics
from utils.repository import device_data

app = FastAPI(
    title="Analysis system",
    docs_url="/"
)


@app.post("/data", status_code=status.HTTP_201_CREATED)
async def add_device_data(data: DevDataCreate, session: SessionDep) -> DevDataCreate:
    res = await device_data.create_data(data, session)
    return res


@app.get("/data/{device_id}", response_model=list[DeviceStatistics])
async def get_device_data(device_id: str, session: SessionDep):
    res = await device_data.get_data(device_id, session)
    return res


@app.get("/data/analysis/{device_id}")
async def analyze_data_period(
        session: SessionDep,
        device_id: str,
        start_date: datetime = datetime.utcfromtimestamp(0),
        end_date: datetime = datetime.utcnow()
):
    res = await device_data.analysis_data(session, device_id, start_date, end_date)
    return res

