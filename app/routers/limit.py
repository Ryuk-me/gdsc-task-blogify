from fastapi import APIRouter as __APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
router = __APIRouter(
    prefix='/limit',
    tags=['Check limit 1 time 5 seconds'],
    redirect_slashes=False
)


@router.get('/', dependencies=[Depends(RateLimiter(times=1, seconds=5))], description="Endpoint to test Ratelimit 1 time 5 seconds")
async def __limit_check():
    return {"success": 200}
