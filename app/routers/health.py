from fastapi import APIRouter as __APIRouter


router = __APIRouter(
    prefix='/healthchecker',
    tags=['Check Health'],
    redirect_slashes=False
)


@router.get('/')
async def __check_health():
    return {"success": 200}
