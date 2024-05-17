from fastapi import APIRouter, Depends, status, BackgroundTasks

from src.exceptions import InvalidCredentials, NotFoundException
from src.auth.service import UserAuthService
from src.auth.dependencies import get_user_auth_service, get_current_user_from_token
from src.auth.schemas import CreateUser, ShowUser, Token, LoginForm
from src.auth.responses import auth_signup_responses, auth_signin_responses
from src.auth.jwt import create_access_token
from src.util.email_util import Email


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser,
    responses={**auth_signup_responses},
)
async def create_user(
    new_user: CreateUser,
    background_task: BackgroundTasks,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    user = await user_auth_service.create(user_data=new_user)
    background_task.add_task(Email.send_verify_email, user)

    return user


@auth_router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={**auth_signin_responses},
)
async def login_for_access_token(
    form_data: LoginForm,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    user = await user_auth_service.authentificate_user(
        form_data.login, form_data.password
    )
    if not user:
        raise InvalidCredentials(detail="Incorrect login or password")

    access_token = create_access_token(data={"sub": form_data.login})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/verification/{token}")
async def email_verivication(
    token: str, user_auth_service: UserAuthService = Depends(get_user_auth_service)
):
    try:
        user = await get_current_user_from_token(token, user_auth_service)
        if user.is_verified:
            message = "The email has already been confirmed"
        else:
            await user_auth_service.verified_user(user)
            message = "The email has been successfully confirmed"
    except:
        raise NotFoundException(detail="Invalid link")
    else:
        return {"message": message}
