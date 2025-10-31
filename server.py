from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time
from .routes import validate_key, login, queue, status, devices
# useless commit
app = FastAPI()

app.state.start_time = time.time()
app.include_router(validate_key.router)
app.include_router(login.router)
app.include_router(queue.router)
app.include_router(status.router)
app.include_router(devices.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/uptime")
async def get_uptime():
    uptime = int(time.time() - app.state.start_time)
    return {"uptime": uptime}

@app.get("/")
async def root():
    return FileResponse("public/index.html")
