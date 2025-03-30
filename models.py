from sqlalchemy import Column, String, Integer, DateTime
import datetime
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id              = Column(Integer, primary_key=True, index=True)
    original_url    = Column(String, nullable=False)
    short_url       = Column(String, unique=True, index=True, nullable=False)
    clicks          = Column(Integer, default=0)
    expiration_date = Column(DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(days=3))