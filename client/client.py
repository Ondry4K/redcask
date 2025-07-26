# this is gonna take a shit ton of time i already know it
import os
from dotenv import load_dotenv
import colorama
import libtorrent as lt
import logging
import requests
import base64
import time
import uuid
import json
import sys

# .env
dotenv = load_dotenv()

# server conf
s_key = base64.b64encode(os.getenv("server_key").encode()).decode()
s_ip = os.getenv("server_ip")
s_port = os.getenv("port")
base = f"http://{s_ip}:{s_port}/"
auth_header = { "Authorization": f"{s_key}" }

# client identificaiton for /login
def get_ip():
    r = requests.get("https://api.ipify.org")
    ip = r.text
    return ip

client = {
    "ip": str(get_ip()),
    "hwid": str(uuid.getnode()),
}

def get_uuid():
    r = requests.post(f"{base}/login", headers=auth_header, json=client)
    json_response = r.json()
    return json_response["uuid"]

# queue mechanism
def rem_queue(d_uuid, d_magnet):
    #to remove an item from queue
    del_scheme = {
        "uuid": d_uuid,
        "magnet_link": d_magnet
    }
    r = requests.delete(f"{base}/queue", headers=auth_header, json=del_scheme)
def get_queue():
    r = requests.get(f"{base}/queue", headers=auth_header)
    json_response = r.json()
    items = json_response["queue"]
    for item in items:
        queue.update({
            "uuid": item["uuid"],
            "magnet_link": item["magnet_link"]
        })
def start_queue():
    q_uuid = queue.get("uuid")
    q_magnet = queue.get("magnet_link")
    print(queue)
    for item in queue:
        if queue.get("uuid") == c_uuid:
            logging.info(f"Download starting - {q_magnet}")
            time.sleep(5)
            topop = next(iter(queue.keys()))
            queue.pop(topop)
            rem_queue(q_uuid, q_magnet)
            time.sleep(5)
            start_download_magnet(q_magnet)
        else:
            while q_uuid != c_uuid:
                logging.info("No torrent for this client, waiting...")
                time.sleep(25)
        
# handle magnet downloads
def start_download_magnet(magnet):
    session = lt.session()
    # session.listen_on(6881, 6891)  # deprecated

    save_path = os.getenv("save_path", "./downloads")

    params = lt.parse_magnet_uri(magnet)
    params.save_path = save_path

    handle = session.add_torrent(params)
    logging.info("added, fetching metadata")

    while not handle.status().has_metadata:
        logging.info("waiting for metadata")
        time.sleep(1)

    logging.info("Metadata received: %s", handle.status().name)

    while not handle.status().is_seeding:
        status = handle.status()

        logging.info(
            '%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s',
            status.progress * 100,
            status.download_rate / 1000,
            status.upload_rate / 1000,
            status.num_peers,
            status.state
        )

        status_body = {
            "name": str(handle.status().name),
            "uuid": str(c_uuid),
            "progress": status.progress * 100
        }
        
        r = requests.post(f"{base}/status", headers=auth_header, json=status_body)
        if r.status_code != 200:
            logging.ERROR("failed to update status: %s", r.text)
        else:
            logging.info("status updated successfully")
        
        time.sleep(30)

    logging.info("complete: %s", handle.status().name)
    


queue = {}
c_uuid = str(get_uuid()) # client UUID

# startup stuff
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
colorama.init(autoreset=True)
logging.info(f"Client UUID: {c_uuid}")

get_queue()
start_queue()


    
    