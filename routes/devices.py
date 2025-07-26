# very simple route, lists all devices registered in the devices.csv file

from fastapi import APIRouter, Header, HTTPException
import csv
from ..depends import is_authorized

router = APIRouter()

@router.get("/devices")
async def get_devices(Authorization: str = Header(...)):
    if not is_authorized(Authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    devices = []
    try:
        with open("./devices.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    devices.append({
                        "uuid": row[0],
                        "ip": row[1]
                    })
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Devices file not found")
    
    return {"devices": devices}