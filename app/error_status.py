from fastapi import HTTPException, status

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=f'user not found')

USER_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="user already exist")

BLOG_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

INVALID_ID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="invalid id")

INVALID_LIMIT = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="invalid limit")

INVALID_TITLE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="invalid search text")

INVALID_SEARCH_TEXT = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="invalid search text")

NO_RESULT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="no result found")

INVALID_USERNAME = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="invalid username format")

TOKEN_CREDENTIALS_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
