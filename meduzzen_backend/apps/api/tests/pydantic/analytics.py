from datetime import datetime

from pydantic import BaseModel


class AnalyticsBody(BaseModel):
    start_date: datetime
    end_date: datetime
