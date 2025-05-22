from fastapi import APIRouter
from pymongo import AsyncMongoClient
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/api")
mongo = AsyncMongoClient("mongodb://localhost:27017")
db = mongo["Elijah"] 
collection = db["widget_logs"]

@router.get("/client_raw_counts")
async def get_client_raw_counts():
    cursor = collection.find({}, {"_id": 0, "timestamp": 1, "email": 1, "client_id": 1})
    docs = await cursor.to_list(length=None)

    # group by timestamp + email + client_id (optional)
    # remove duplicates if necessary
    # OR: group here into minute buckets if needed

    return docs
