from sanic import Sanic, text, html, HTTPResponse, file
import os
import base64

app = Sanic("MyHelloWorldApp")
app.extend()

# Define a route to serve static files
app.static('/imgs', './imgs')

TEST_USERS = [
    {'name': 'kilo', 'password': 'kilo1234'},
    {'name': 'admin', 'password': 'admin1234'},
]

AUTH_RESPONSE = HTTPResponse(
    status=401,
    headers={'WWW-Authenticate': 'Basic realm="Login Required"'},
    body='Unauthorized'
)


def check_credentials(content: str):
    decoded_credentials = base64.b64decode(content).decode('utf-8')
    username, password = decoded_credentials.split(':')

    for user in TEST_USERS:
        if username == user['name'] and password == user['password']:
            return True
    return False


def check_basicauth(request):
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


@app.get("/")
async def index(request):
    if not check_basicauth(request):
        return AUTH_RESPONSE
    try:
        with open('index.html', 'r') as f:
            index_data = f.read()
        got_file = True
    except FileNotFoundError as e:
        got_file = False
    if got_file:
        return html(index_data)
    else:
        return text("We could not find index.html")


@app.get("/pics")
async def get_pics(request):
    if not check_basicauth(request):
        return AUTH_RESPONSE
    try:
        with open('pics.html', 'r') as f:
            index_data = f.read()
        got_file = True
    except FileNotFoundError as e:
        got_file = False
    if got_file:
        return html(index_data)
    else:
        return text("We could not find index.html")


@app.route('/images/<name>')
async def hello(request, name):
    if not check_basicauth(request):
        return AUTH_RESPONSE

    filename = name + '.png'
    if not os.path.exists(filename):
        return text(f'{filename} does not exists')

    return await file(filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
