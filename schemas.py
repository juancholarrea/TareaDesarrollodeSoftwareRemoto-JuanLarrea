from pydantic import BaseModel
import datetime

class URLBase(BaseModel):
    url: str  

class URLCreate(URLBase):
    pass

class URLResponse(BaseModel):
    original_url: str
    short_url: str
    expiration_date: datetime.datetime

    class Config:
        orm_mode = True
