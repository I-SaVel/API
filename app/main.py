from fastapi import FastAPI, Depends, HTTPException
from app.database import SessionLocal, engine
from .schema import DeviceInfo, Configuration
from . import models
from app import crud
import os
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
SECRET_KEY = os.getenv("SECRET_KEY")

def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post('/device/info')
def save_device_info(info: DeviceInfo, db=Depends(db)):
    object_in_db = crud.get_device_info(db, info.token)
    if object_in_db:
        raise HTTPException(400, detail= crud.error_message('This device info already exists'))
    return crud.save_device_info(db, info)

@app.get('/device/info/{token}')
def get_device_info(token: str, db=Depends(db)):
    info = crud.get_device_info(db, token)
    if info:
        return info
    else:
        raise HTTPException(404, crud.error_message('No device found for token {}'.format(token)))

@app.get('/device/info')
def get_all_device_info(db=Depends(db)):
    return crud.get_device_info(db)

@app.post('/configuration')
def save_configuration(config: Configuration, db=Depends(db)):
    crud.delete_nudges_configuration(db)
    return crud.save_nudges_configuration(db, config)

@app.get('/configuration')
def get_configuration(db=Depends(db)):
    config = crud.get_nudges_configuration(db)
    if config:
        return config
    else:
        raise HTTPException(404, crud.error_message('No configuration set'))
@app.get("/")
async def root():
    return {"message": "Hello World "+SECRET_KEY}

@app.delete('/device/info/delete/{token}')
async def delete_device_info(token: str, db=Depends(db)):
    config = crud.delete_device_info(db, token)
    if config:
        return config
    else: raise HTTPException(404, crud.error_message('No device found for token {}'.format(token)))

@app.put('/device/info/put/')
async def delete_device_info(info: DeviceInfo, db=Depends(db)):
    config = crud.update_device_info(db, info)
    if config:
        return config
    else: raise HTTPException(404, crud.error_message('No device found for token {}'.format(token)))