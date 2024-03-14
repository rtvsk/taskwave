from datetime import timedelta

from fastapi import HTTPException
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_async_session
from src.auth.service import authentificate_user, create_access_token
from src.auth.schemas import Token, LoginForm


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/signin",
    responses={
        200: {"model": Token},
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect login or password"}
                }
            },
        },
    },
)
async def login_for_access_token(
    form_data: LoginForm,
    session: AsyncSession = Depends(get_async_session),
):
    user = await authentificate_user(form_data.login, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": form_data.login},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
