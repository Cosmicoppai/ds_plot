from sanic import Request
from .exceptions import InvalidAuthError
import base64


TEST_USERS = {"kilo": "kilo1234", "admin": "admin1234"}


def check_credentials(content: str) -> bool:
    decoded_credentials = base64.b64decode(content).decode('utf-8')
    username, password = decoded_credentials.split(':')

    if username in TEST_USERS and TEST_USERS[username] == password:
        return True
    return False


def check_basicauth(request: Request) -> bool:
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    try:
        auth_type, content = auth_header.split(" ")
        if auth_type.lower() == 'basic':
            if check_credentials(content):
                return True
            else:
                raise ValueError("Not valid user")
        else:
            raise ValueError("Not basic auth")
    except (UnicodeDecodeError, ValueError):
        return False


async def authorize(request):
    if not check_basicauth(request):
        return InvalidAuthError
