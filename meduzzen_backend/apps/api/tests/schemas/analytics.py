from datetime import datetime

from pydantic import BaseModel


class AnalyticsRequestBodySchema(BaseModel):
    start_date: datetime
    end_date: datetime
