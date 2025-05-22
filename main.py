from fastapi import FastAPI
from log_router import router as log_router
from api_router import router as api_router
import uvicorn

app = FastAPI(title="PMv Log Server")
app.include_router(log_router)
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Log server is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=False, http="httptools")