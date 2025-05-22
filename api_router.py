from fastapi import APIRouter
from pymongo import AsyncMongoClient
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/api")
mongo = AsyncMongoClient("mongodb://localhost:27017")
db = mongo["Elijah"] 
collection = db["widget_logs"]

@router.get("/widget_usage")
async def get_widget_usage():
    pipeline = [
        { "$project": {
            "timestamp": 1,
            "email": 1,
            "widgets": { "$objectToArray": "$widgets" }
        }},
        { "$unwind": "$widgets" },
        { "$project": {
            "timestamp": 1,
            "email": 1,
            "widget_name": "$widgets.k",
            "count": "$widgets.v"
        }},
        { "$sort": { "timestamp": 1 } }
    ]

    cursor = collection.aggregate(pipeline)
    results = [doc async for doc in cursor]
    return results

