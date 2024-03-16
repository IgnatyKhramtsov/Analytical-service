from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from database import Base

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class DeviceData(Base):
    __tablename__ = "device_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str]
    timestamp: Mapped[created_at]
    x: Mapped[float]
    y: Mapped[float]
    z: Mapped[float]
