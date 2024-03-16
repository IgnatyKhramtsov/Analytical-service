from datetime import datetime

from pydantic import BaseModel


class DeviceStatistics(BaseModel):
    x: float
    y: float
    z: float


class DevDataCreate(DeviceStatistics):
    device_id: str


class DevData(DevDataCreate):
    id: int
    timestamp: datetime


class AnalData(BaseModel):
    # device_id: str
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    sum_x: float
    sum_y: float
    sum_z: float
    count_x: int
    count_y: int
    count_z: int
    median_x: float
    median_y: float
    median_z: float




