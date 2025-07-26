# VERY important part of the API
# this part is relatively simple, what it does is it validates the key in any given request and returns whether it's correct
# the key is specified in the .env file, and it should be sent in the request header as 'Authorization'

# POST: validate key (passed as the content of the request, hashed using base64), we can then return either a boolean or we can implement a 200 or 401 response (probably the second option)

from fastapi import APIRouter
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
import base64

router = APIRouter()

load_dotenv(dotenv_path=Path("./.env"))

class Auth(BaseModel):
    Authorization: str

@router.post("/validate_key")
async def validate_key(auth: Auth):
    envkey = os.getenv("KEY")
    key = base64.b64encode(envkey.encode()).decode()
    if auth.Authorization == key:
        return True
    else:
        return False
        # alternatively, we can return a 401 response
        # from fastapi.responses import JSONResponse
        # return JSONResponse(status_code=401, content={"message": "Unauthorized"})