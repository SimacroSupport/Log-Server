from fastapi import APIRouter
from pymongo import AsyncMongoClient
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api")
mongo = AsyncMongoClient("mongodb://localhost:27017")
db = mongo["Elijah"] 
collection = db["widget_logs"]

@router.get("/widget_usage")
async def get_widget_usage():
    pipeline = [
        {
            "$project": {
                "timestamp": 1,
                "email": 1,
                "widgets": { "$objectToArray": "$widgets" }
            }
        },
        { "$unwind": "$widgets" },
        {
            "$project": {
                "_id": 0,
                "timestamp": 1,
                "metric": {
                    "$concat": ["$email", " / ", "$widgets.k"]
                },
                "value": "$widgets.v"
            }
        },
        { "$sort": { "timestamp": 1 } }
    ]

    cursor = await collection.aggregate(pipeline, allowDiskUse=True)
    results = [doc async for doc in cursor]
    for doc in results:
        doc.pop("_id", None)
        if isinstance(doc["timestamp"], datetime):
            doc["timestamp"] = doc["timestamp"].isoformat() + "Z"

        
    return results

