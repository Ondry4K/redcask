# very simple part of the api
# crucial to registering clients to our device pool, which can be assigned torrents in the queue
# each device gets a UUID that's HWID based so it doesn't dynamically change, (we'll implement this in the client)
# if a device is not yet registered it sends a POST request to this route with its HWID and local IP
# the server then returns a UUID which the device is assigned, allowing it to be differentiated from other devices

# authorization applies here to so someone random can't register
# every device is stored in devices.csv, which is a simple csv file with the following format:
# UUID,IP

from fastapi import APIRouter, Header, HTTPException
import csv
from pydantic import BaseModel
import uuid
from pathlib import Path
from ..depends import is_authorized

namespace = uuid.UUID("4473adca-0ca2-4ba3-83ff-2157937463dd") # this represents the string "LOGIN", we want a namespace to have persistent UUIDs for the same devices
router = APIRouter()

class Device(BaseModel):
    hwid: str
    ip: str

def check_device(target_uuid):
    with open("./devices.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == str(target_uuid):
                return True
        return False
    

@router.post("/login")
async def login(device: Device, Authorization: str = Header(...)):
    if not is_authorized(Authorization): # this one check cost me like 30 minutes of my life
        raise HTTPException(status_code=401, detail="Unauthorized")
    device_uuid = uuid.uuid5(namespace, device.hwid)
    ip = device.ip
    result = check_device(device_uuid)
    if result == True:
        status = "Already exists, didn't write."
    else:
        with open("./devices.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([str(device_uuid)] + [ip])
            status = "Success"
    if status == "Already exists, didn't write.":
        return {"status": status, "uuid": str(device_uuid), "ip": ip}
    else:
        return {"status": status, "uuid": str(device_uuid), "ip": ip}
    
# note: absolute headache to code