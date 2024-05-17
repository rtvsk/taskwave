from src.responses import common_validation_response
from src.auth.responses import credentials_error_response

users_edit_responses = {
    **common_validation_response,
    **credentials_error_response,
    400: {
        "description": "At least one parameter for user update info should be provided"
    },
}
