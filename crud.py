from sqlalchemy.orm import Session
import models, schemas
import utils
import datetime

def create_short_url(db: Session, original_url: str):
    original_url    = str(original_url)  
    short_url       = utils.generate_short_url()
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    
    db_url = models.URL(
        original_url=original_url,
        short_url=short_url,
        expiration_date=expiration_date
    )
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_original_url(db: Session, short_url: str):
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url, models.URL.expiration_date > datetime.datetime.utcnow()).first()
    if db_url:
        db_url.clicks += 1
        db.commit()
    return db_url.original_url if db_url else None

def get_click_count(db: Session, short_url: str):
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    return db_url.clicks if db_url else 0