from fastapi import FastAPI

app = FastAPI()

# Example: Return static JSON for a given token_id
@app.get("/metadata/{token_id}")
def get_metadata(token_id: int):
    # For MVP, just return a hard-coded JSON or something dynamic
    return {
        "name": f"My NFT #{token_id}",
        "description": "An awesome NFT",
        "image": f"https://example.com/images/{token_id}.png",
        "attributes": []
    }
