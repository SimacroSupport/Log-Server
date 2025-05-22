from fastapi import APIRouter
from pymongo import AsyncMongoClient
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")
mongo = AsyncMongoClient("mongodb://localhost:27017")
db = mongo["Elijah"] 
collection = db["widget_logs"]

@router.get("/api/client_counts")
async def get_client_counts():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "email": "$email",
                    "hour": { "$dateTrunc": { "date": "$timestamp", "unit": "hour" } }
                },
                "client_ids": { "$addToSet": "$client_id" }
            }
        },
        {
            "$project": {
                "email": "$_id.email",
                "hour": "$_id.hour",
                "client_count": { "$size": "$client_ids" }
            }
        },
        { "$sort": { "hour": 1 } }
    ]

    cursor = collection.aggregate(pipeline)
    results = [doc async for doc in cursor]
    return JSONResponse(content=results)