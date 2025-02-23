import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve the metadata folder as static files
app.mount("/metadata", StaticFiles(directory="metadata"), name="metadata")

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
def get_nft_metadata(token_id: str):
    """Fetch metadata for a specific NFT based on token ID."""
    metadata_path = os.path.join(METADATA_DIR, f"{token_id}.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail=f"NFT metadata for token {token_id} not found")

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")
