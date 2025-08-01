from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from typing import List, Union
from datetime import datetime
import re

router = APIRouter(prefix="/logs")
mongo = AsyncMongoClient("mongodb://localhost:27017")
meta_db = mongo["log_meta"]


class WidgetLog(BaseModel):
    timestamp: datetime
    email: Union[str, None] = None  # 에러방지
    client_id: Union[str, None] = None  # 에러방지
    widgets: dict


class LogPayload(BaseModel):
    logs: List[WidgetLog]


@router.post("/{server_id}")
async def receive_logs(server_id: str, payload: LogPayload):
    if not re.match(r"^[a-zA-Z0-9_\-.]{1,64}$", server_id):
        return {"status": "error", "message": "Invalid server_id"}

    db = mongo[server_id]

    if "widget_logs" not in await db.list_collection_names():
        try:
            await db.create_collection(
                "widget_logs",
                timeseries={"timeField": "timestamp", "metaField": "email", "granularity": "minutes"},  # optional
            )
            await db["widget_logs"].create_index("timestamp")
            print(f"[🆕] Created time-series collection for {server_id}")
        except Exception as e:
            return {"status": "error", "message": str(e)}

        await meta_db["servers"].insert_one({"server_id": server_id, "created_at": datetime.utcnow()})
    try:
        logs = [log.dict() for log in payload.logs]
        logs = [log for log in logs if log["email"] is not None]  # Email
        await db["widget_logs"].insert_many(logs)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "ok", "inserted": len(logs)}
