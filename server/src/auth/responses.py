from src.responses import common_validation_response

auth_signup_responses = {
    **common_validation_response,
    409: {"description": "User with this login or email already exists"},
}

auth_signin_responses = {
    **common_validation_response,
    401: {"description": "Incorrect login or password"},
}


credentials_error_response = {401: {"description": "Could not validate credentials"}}
