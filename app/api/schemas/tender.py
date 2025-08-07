from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TenderBase(BaseModel):
    title: str
    start_price: Optional[float] = None
    place_of_delivery: str
    url: str
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)

class TenderCreate(TenderBase):
    number: int

class TenderRead(TenderBase):
    number: int

    model_config = {
        "from_attributes": True
    }