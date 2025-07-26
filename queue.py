#DEPENDANT ON REQUEST METHOD
# POST: add torrent to queue (MUST include the UUID of the device which we want to assign the torrent to)
# GET: get queue
# DELETE: delete torrent from queue (MUST include the UUID of the device which we want to delete the torrent from)

# AUTHORIZATION
# authorization works by checking against validate_key when sending a request
# the authorization header should include your key specified in .env (server)
# the client which only does 2 requests; a get request to receive the torrent file/magnet from the queue and a delete request to remove it when its downloading
# after the client deletes the torrent from the queue (which means it got it), it will send a request to the status route
# from there it should be visible that the torrent is downloading along with the ETA, size downloaded, peers and leachers

# SAVING REQUESTS
# since we want some consistency, we need a csv file to (TEMPORARILY) save the queue
# its a format of UUID,torrent_file/magnet,timestamp
# if we want to get the queue we check the csv file to see if there are any entries and format them for displaying the queue

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
from ..depends import is_authorized
import csv

router = APIRouter()

class QueueItem(BaseModel):
    uuid: str
    magnet_link: str

def check_item(uuid: str, magnet_link: str) -> bool:
    with open("./queue.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == uuid and row[1] == magnet_link:
                return True
    return False

@router.get("/queue")
async def get_queue(Authorization: str = Header(...)):
    if not is_authorized(Authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with open ("./queue.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        queue = []
        for row in reader:
            if row:
                queue.append({
                    "uuid": row[0],
                    "magnet_link": row[1]
                })
    return {"queue": queue}

@router.post("/queue")
async def add_queue(Item: QueueItem, Authorization: str = Header(...)):
    if not is_authorized(Authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    exists = check_item(Item.uuid, Item.magnet_link)
    if exists == True:
        raise HTTPException(status_code=400, detail="Item already exists in queue")
    else:
        with open("./queue.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([Item.uuid, Item.magnet_link])
        return {"status": "success", "message": "Torrent added to queue"}
    
@router.delete("/queue")
async def del_queue(Item: QueueItem, Authorization: str = Header(...)):
    if not is_authorized(Authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    exists = check_item(Item.uuid, Item.magnet_link)
    if exists == False:
        raise HTTPException(status_code=404, detail="Item not found in queue")
    else:
        with open("./queue.csv", mode="r", newline="") as file:
            lines = file.readlines()
        with open("./queue.csv", mode="w", newline="") as file:
            for line in lines:
                if line.strip() != f"{Item.uuid},{Item.magnet_link}":
                    file.write(line)
        return {"status": "success", "message": "Torrent removed from queue"}