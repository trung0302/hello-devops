# file: app/main.py
"""hello-devops: app mẫu dùng xuyên suốt lộ trình."""
import os

from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="hello-devops")

HTTP_REQUESTS = Counter(
    "http_requests",
    "HTTP requests by path and status code",
    ["path", "status"],
)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    HTTP_REQUESTS.labels(request.url.path, str(response.status_code)).inc()
    return response

@app.get("/")
def root():
    return {"message": "hello devops", "version": APP_VERSION}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/fail")
def fail():
    raise HTTPException(status_code=500, detail="simulated failure")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
