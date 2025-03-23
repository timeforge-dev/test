import os
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI()

# OPTIONAL: A custom handler that returns more info when a 404 occurs.
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"detail": f"Path not found: {request.url.path}"},
        status_code=404
    )

METADATA_DIR = "metadata"

# Root endpoint (GET, HEAD) just to confirm service is running.
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return JSONResponse(content={"message": "Immutable Metadata API Running"}, status_code=200)

# Optional endpoint for "/metadata" if IMX or other explorers ping it directly
@app.api_route("/metadata", methods=["GET", "HEAD"])
def list_metadata():
    """
    Returns a friendly message or instructions for how to access collection or token metadata.
    """
    return JSONResponse(
        content={"message": "Use /metadata/collection.json or /metadata/{tokenId} to access metadata."},
        status_code=200
    )

@app.api_route("/metadata/collection.json", methods=["GET", "HEAD"])
def get_collection_metadata():
    """
    Returns metadata for the entire NFT collection in Immutable's format.
    Expects a file named 'collection.json' in the 'metadata' folder.
    """
    metadata_path = os.path.join(METADATA_DIR, "collection.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Collection metadata not found")

    if "HEAD" in Request.method:
        # HEAD requests don’t require sending JSON content, just let them know it's there
        return Response(status_code=200)

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")

@app.api_route("/metadata/{token_id}", methods=["GET", "HEAD"])
def get_nft_metadata(token_id: str):
    """
    Returns metadata for a specific NFT by token ID, following Immutable's format.
    Expects a file named '{token_id}.json' in the 'metadata' folder.
    """
    metadata_path = os.path.join(METADATA_DIR, f"{token_id}.json")

    if not os.path.exists(metadata_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Metadata for token {token_id} not found"
        )

    if "HEAD" in Request.method:
        # HEAD request: just return 200 if file exists
        return Response(status_code=200)

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return JSONResponse(content=metadata, media_type="application/json")
