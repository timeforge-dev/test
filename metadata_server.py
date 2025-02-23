from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import json

app = FastAPI()

METADATA_DIR = "metadata"

@app.get("/", methods=["GET", "HEAD"])
def root():
    return JSONResponse(content={"message": "Immutable Metadata API Running"}, status_code=200)

@app.get("/metadata/collection.json")
def get_collection_metadata():
    """Returns metadata for the NFT collection, following Immutable's format."""
    metadata_path = os.path.join(METADATA_DIR, "collection.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Collection metadata not found")

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")

@app.get("/metadata/{token_id}")
def get_nft_metadata(token_id: str):
    """Returns metadata for a specific NFT by token ID, following Immutable's format."""
    metadata_path = os.path.join(METADATA_DIR, f"{token_id}.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail=f"Metadata for token {token_id} not found")

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")
