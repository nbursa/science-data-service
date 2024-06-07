from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_comments():
    return {"message": "List of comments"}
