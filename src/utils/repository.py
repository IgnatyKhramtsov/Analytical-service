from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, and_, func, cast, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from device.models import DeviceData
from device.schemas import DevDataCreate, DeviceStatistics, DevData, AnalData


class SQLAlchemyDeviceRepository:
    model = DeviceData

    async def create_data(self, data: DevDataCreate, session: AsyncSession) -> DevDataCreate:
        data = data.model_dump()
        db_data = self.model(**data)
        session.add(db_data)
        await session.commit()
        return db_data

    async def get_data(self, device_id: str, session: AsyncSession) -> DeviceStatistics:
        query = select(self.model.x, self.model.y, self.model.z).where(self.model.device_id == device_id)
        res = await session.execute(query)
        result = res.all()
        if not result:
            raise HTTPException(status_code=404, detail="Data not found")
        result_dto = [DeviceStatistics.model_validate(row, from_attributes=True, strict=False) for row in result]
        return result_dto

    async def analysis_data(self, session: AsyncSession, device_id: str, start_date: Optional[datetime], end_date: Optional[datetime]):
        query = (
            select(
                # self.model.device_id,
                func.min(self.model.x).label("min_x"),
                func.min(self.model.y).label("min_y"),
                func.min(self.model.z).label("min_z"),
                func.max(self.model.x).label("max_x"),
                func.max(self.model.y).label("max_y"),
                func.max(self.model.z).label("max_z"),
                cast(func.sum(self.model.x), Numeric(precision=5, scale=2)).label("sum_x"),
                cast(func.sum(self.model.y), Numeric(precision=5, scale=2)).label("sum_y"),
                cast(func.sum(self.model.z), Numeric(precision=5, scale=2)).label("sum_z"),
                func.count(self.model.x).label("count_x"),
                func.count(self.model.y).label("count_y"),
                func.count(self.model.z).label("count_z"),
                cast(func.percentile_cont(0.5).within_group(
                    self.model.x.desc()), Numeric(precision=5, scale=2)).label("median_x"),
                cast(func.percentile_cont(0.5).within_group(
                    self.model.y.desc()), Numeric(precision=5, scale=2)).label("median_y"),
                cast(func.percentile_cont(0.5).within_group(
                    self.model.z.desc()), Numeric(precision=5, scale=2)).label("median_z")
            )
            .select_from(self.model)
            .where(and_(
                self.model.device_id == device_id,
                self.model.timestamp >= start_date,
                self.model.timestamp <= end_date
            ))
        )
        res = await session.execute(query)
        result = res.all()
        # result = [DevData.model_validate(row, from_attributes=True, strict=False) for row in result]
        result = [AnalData.model_validate(row, from_attributes=True, strict=False) for row in result]
        return result

    async def get_data_for_analyse(self, session: AsyncSession):
        """ select device_id,
            min(x) as min_x,
            min(y) as min_y,
            min(z) as min_z,
            max(x) as max_x,
            max(y) as max_y,
            max(z) as max_z,
            count(x) as count_x,
            count(y) as count_y,
            count(z) as count_z,
            avg(x) as avg_x,
            avg(y) as avg_y,
            avg(z) as avg_z,
            percentile_disc(0.5) WITHIN GROUP (ORDER BY z) AS median_z,
            percentile_disc(0.5) WITHIN GROUP (ORDER BY x) AS median_x,
            percentile_disc(0.5) WITHIN GROUP (ORDER BY y) AS median_y
            from device_data
            group by device_id ;
        """
        query = (
            select(
                # self.model.device_id,
                func.min(self.model.x).label("min_x"),
                func.min(self.model.y).label("min_y"),
                func.min(self.model.z).label("min_z"),
                func.max(self.model.x).label("max_x"),
                func.max(self.model.y).label("max_y"),
                func.max(self.model.z).label("max_z"),
                cast(func.sum(self.model.x), Numeric(precision=5, scale=2)).label("sum_x"),
                cast(func.sum(self.model.y), Numeric(precision=5, scale=2)).label("sum_y"),
                cast(func.sum(self.model.z), Numeric(precision=5, scale=2)).label("sum_z"),
                func.count(self.model.x).label("count_x"),
                func.count(self.model.y).label("count_y"),
                func.count(self.model.z).label("count_z"),
                cast(func.percentile_cont(0.5).within_group(
                    self.model.x.desc()), Numeric(precision=5, scale=2)).label("median_x"),
                cast(func.percentile_cont(0.5).within_group(
                    self.model.y.desc()), Numeric(precision=5, scale=2)).label("median_y"),
                cast(func.percentile_cont(0.5).within_group(
                    self.model.z.desc()), Numeric(precision=5, scale=2)).label("median_z")
            )
            .select_from(self.model)
            # .where(self.model.device_id == 'string')
            .group_by(self.model.device_id)
            # .where(and_(
            #     self.model.device_id == device_id,
            #     self.model.timestamp >= start_date,
            #     self.model.timestamp <= end_date
            # ))
        )
        res = await session.execute(query)
        result = res.all()
        print(f"{result}")
        result = [AnalData.model_validate(row, from_attributes=True, strict=False) for row in result]
        return result




device_data = SQLAlchemyDeviceRepository()
