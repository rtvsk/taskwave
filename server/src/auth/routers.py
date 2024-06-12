import logging
from fastapi import APIRouter, Depends, status, BackgroundTasks

from src.exceptions import NotFoundException
from src.responses import ValidationException
from src.auth.service import UserAuthService
from src.auth.dependencies import get_user_auth_service, get_current_user_from_token
from src.auth.schemas import CreateUser, ShowUser, Token, LoginForm
from src.auth.responses import (
    UserAlreadyExistsException,
    SigninException,
    InvalidLinkException,
)
from src.auth.jwt import JwtToken
from src.util.email_util import email


logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser,
    responses={
        status.HTTP_409_CONFLICT: {"model": UserAlreadyExistsException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
    },
)
async def create_user(
    new_user: CreateUser,
    background_task: BackgroundTasks,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    user = await user_auth_service.create(user_data=new_user)
    background_task.add_task(email.send_verify_email, user)

    return user


@auth_router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": SigninException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
    },
)
async def login_for_access_token(
    form_data: LoginForm,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    await user_auth_service.authentificate_user(form_data.login, form_data.password)
    access_token = JwtToken.create_access_token(data={"sub": form_data.login})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get(
    "/verification/{token}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": InvalidLinkException},
    },
)
async def email_verivication(
    token: str, user_auth_service: UserAuthService = Depends(get_user_auth_service)
):
    try:
        user = await get_current_user_from_token(token, user_auth_service)
        if user.is_verified:
            message = "The email has already been confirmed"
        else:
            logging.debug("Run def verified_user")
            await user_auth_service.verified_user(user)
            logging.debug("User successfully verified")
            message = "The email has been successfully confirmed"
    except Exception as e:
        logging.error(f"Except: {e}")
        raise NotFoundException(detail="Invalid link")
    else:
        return {"message": message}
