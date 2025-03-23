import os
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response

app = FastAPI()

# Custom 404 handler for clearer messages
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"detail": f"Path not found: {request.url.path}"},
        status_code=404
    )

METADATA_DIR = "metadata"

# Root endpoint
@app.api_route("/", methods=["GET", "HEAD"])
def root(request: Request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse(
        content={"message": "Immutable Metadata API Running"},
        status_code=200
    )

# /metadata endpoint (optional, avoids 404 if IMX pings just /metadata)
@app.api_route("/metadata", methods=["GET", "HEAD"])
def list_metadata(request: Request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse(
        content={"message": "Use /metadata/collection.json or /metadata/{tokenId} to access metadata."},
        status_code=200
    )

# Collection-level metadata
@app.api_route("/metadata/collection.json", methods=["GET", "HEAD"])
def get_collection_metadata(request: Request):
    metadata_path = os.path.join(METADATA_DIR, "collection.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Collection metadata not found")

    if request.method == "HEAD":
        return Response(status_code=200)

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")

# Token-level metadata
@app.api_route("/metadata/{token_id}", methods=["GET", "HEAD"])
def get_nft_metadata(token_id: str, request: Request):
    metadata_path = os.path.join(METADATA_DIR, f"{token_id}.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(
            status_code=404,
            detail=f"Metadata for token {token_id} not found"
        )

    if request.method == "HEAD":
        return Response(status_code=200)

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")
