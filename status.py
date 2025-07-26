# this file serves the purpose of getting the status of the torrent (if there are any active) or updating the status
# POST: add status along with the content which includes the info, this is periodically updated by the client, 
# a UUID must be included so the server knows which device is updating this status 
# (proper auth must be passed too as a header)
# GET: gets the current status of the torrent, eg. size downloaded/left, peers, leachers and the ETA.

# SAVING REQUESTS
# for consistency sake (again), we will save the status in a csv file, along with the timestamp 
# (which is updated when the status is, making it sort of like a Last updated timestamp)
# the name of this file (you won't believe this) is status.csv

# standard auth, same as everywhere else, using headers

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
import csv
import os
from ..depends import is_authorized

router = APIRouter()

class Status(BaseModel):
    name: str
    uuid: str
    progress: float
    
def check_exists(uuid: str, name: str) -> bool:
    with open("./status.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name and row[1] == uuid:
                return True
        return False
    
@router.get("/status")
async def get_status(Authorization: str = Header(...)):
    if not is_authorized(Authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")

    statuses = []
    with open("./status.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                try:
                    statuses.append({
                        "name": row[0],
                        "uuid": row[1],
                        "progress": float(row[2])
                    })
                except ValueError:
                    statuses.append({
                        "name": row[0],
                        "uuid": row[1],
                        "progress": None
                    })

    return statuses

@router.post("/status")
async def up_status(status: Status, Authorization: str = Header(...)):
    if not is_authorized(Authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")

    rows = []
    updated = False
    if os.path.exists("./status.csv"):
        with open("./status.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == status.name and row[1] == status.uuid:
                    rows.append([status.name, status.uuid, status.progress])
                    updated = True
                else:
                    rows.append(row)
    if not updated:
        rows.append([status.name, status.uuid, status.progress])
    with open("./status.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return {
        "status": "updated" if updated else "created",
        "name": status.name,
        "uuid": status.uuid,
        "progress": status.progress
    }

        