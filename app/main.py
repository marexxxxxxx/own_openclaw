from fastapi import FastAPI

app = FastAPI(title="own_openclaw API Gateway")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "own_openclaw API Gateway is running"}
