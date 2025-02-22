import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

METADATA_DIR = "metadata"

@app.get("/metadata/collection.json")
def get_collection_metadata():
    """Fetch the collection metadata JSON."""
    metadata_path = os.path.join(METADATA_DIR, "collection.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Collection metadata not found")

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")


@app.get("/metadata/{token_id}")
def get_nft_metadata(token_id: int):
    """Fetch metadata for a specific NFT based on token ID."""
    metadata_path = os.path.join(METADATA_DIR, f"{token_id}.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="NFT metadata not found")

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")
