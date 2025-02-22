import json
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

METADATA_DIR = "metadata"

@app.get("/metadata/{token_id}")
def get_metadata(token_id: int):
    """Fetch NFT metadata from JSON file."""
    metadata_path = os.path.join(METADATA_DIR, f"{token_id}.json")
    
    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    with open(metadata_path, "r") as file:
        metadata = json.load(file)
    
    return metadata
