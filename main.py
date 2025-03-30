from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)
db.close()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
#############################
# EndPoints
#############################
        
@app.get("/")
def read_root():
    return {"message": "Bienvenido al servicio de acortamiento de URLs. Visita /docs para más detalles."}        

@app.post("/shorten/", response_model=schemas.URLResponse)
def create_short_url(url_data: schemas.URLCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_short_url(db, url_data.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/{short_url}")
def redirect_url(short_url: str, db: Session = Depends(get_db)):
    original_url = crud.get_original_url(db, short_url)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found or expired")
    return {"redirect": original_url}

@app.get("/{short_url}/clicks")
def get_click_count(short_url: str, db: Session = Depends(get_db)):
    return {"clicks": crud.get_click_count(db, short_url)}