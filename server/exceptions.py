from sanic import HTTPResponse

InvalidAuthError: HTTPResponse = HTTPResponse(status=401,
                                              headers={'WWW-Authenticate': 'Basic realm="Login Required"'},
                                              body='Unauthorized')
