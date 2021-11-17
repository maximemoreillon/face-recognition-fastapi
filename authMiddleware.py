from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import requests

class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, options={}):
        super().__init__(app)
        self.url = options.get("url", None)
        self.session = requests.Session()
        self.session.trust_env = False

    # The middleware part
    async def dispatch(self, request, call_next):

        # Check for JWT cookie and header
        jwt = self.retrieve_jwt(request)

        # Prevent further execution if no JWT
        if not jwt:
            return JSONResponse({"message": "Missing JWT"}, status_code=403)

        auth_result, status_code = self.verify_jwt(jwt)

        # Unless OK, prevent further execution
        if status_code != 200:
            request.state.user = None
            return JSONResponse(auth_result, status_code=status_code)

        response = await call_next(request)
        return response

    def retrieve_jwt(self, request):
        # Retrieve JWT from either auth header or cookies

        jwt = None

        authorization_header = request.headers.get("Authorization", None)
        if authorization_header:
            jwt = authorization_header.split(" ")[1]

        if not jwt:
            jwt = request.cookies.get("jwt", None)

        return jwt


    def verify_jwt(self, jwt):
        # Validates the JWT by calling the auth microservice

        headers = {"Authorization": f"Bearer {jwt}"}
        response = self.session.get(f"{self.url}", headers=headers)

        if response.status_code != 200:
            return response.text, response.status_code

        user = response.json()
        return user, response.status_code
