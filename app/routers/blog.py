from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse,HTMLResponse

router = APIRouter()

@router.get("/healthz")
async def ping():
    return JSONResponse(
        status_code=200,
        content={"detail": "API up"}
    )

@router.post("/submit")
async def submit_post():
    return NotImplemented

@router.get("/posts")
async def get_all_posts():
    return NotImplemented

@router.get("/posts/{post_id}/view", response_class=HTMLResponse)
async def get_post(post_id: int):
    return NotImplemented
