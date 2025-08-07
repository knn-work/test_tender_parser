from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Tender(Base):
    __tablename__ = "tenders"

    number: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    start_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    place_of_delivery: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    end_time: Mapped[datetime] = mapped_column(DateTime)

