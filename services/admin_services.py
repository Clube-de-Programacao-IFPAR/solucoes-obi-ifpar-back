from dotenv import load_dotenv
import os
from flask import request
import jwt
from ..scripts import get_urls
from ..scripts import download_answers
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ..dtos.login_dto import LoginDTO
from ..dtos.auth_dto import AuthDTO
from ..dtos.reset_password_dto import ResetPasswordDTO
from ..errors.unauthorized import Unauthorized
from ..errors.forbidden import Forbidden
from ..errors.invalid_field import InvalidField
from ..errors.missing_field import MissingField

load_dotenv()

JWT_SECRET_KEY = os.getenv("ADMIN_JWT_SECRET_KEY")

if JWT_SECRET_KEY is None:
    print("Include in the .env the ADMIN_JWT_SECRET_KEY")
    exit(1)

if os.getenv("ADMIN_PASSWORD") is None:
    print("Include in the .env the ADMIN_PASSWORD")
    exit(1)

# default for now just for testing
admin_user = "admin"
admin_pass = generate_password_hash(os.getenv("ADMIN_PASSWORD"))

jwt_count = 0

def is_admin(username, password):
    if username == admin_user and check_password_hash(admin_pass, password):
        return True


def login(data: LoginDTO):
    global jwt_count
    # returns a new token that authorizes admin for the given username and password
    # match username and password with the ones stored in the global variables
    username = data.get("username")
    if username is None:
        raise MissingField("Missing \"username\" field in body")
    password = data.get("password")
    if password is None:
        raise MissingField("Missing \"password\" field in body")
    
    if is_admin(username, password):
        # send a token to the user for auth
        payload: AuthDTO = {
            "username": username,
            "role": "admin",
            "sub": str(jwt_count)
        }
        
        jwt_count += 1
        
        return {
            "token": jwt.encode(payload, key=JWT_SECRET_KEY, algorithm="HS256")
            }, 200
    else:
        raise Unauthorized("Incorrect username or password")


def requires_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #TODO: add an error message to the thingies
        auth_header = request.headers.get('Authorization', type=str)
        if not auth_header:
            raise Unauthorized("Missing \"Authorization\" header")
        parts = auth_header.split() # should be: ['Bearer', jwt]
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise Unauthorized("Authorization header value is not a Bearer token")
        
        token = parts[1]
        try:
            # signatures are auto-verified
            decoded: AuthDTO = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidSignatureError:
            raise Forbidden("JWT signature is invalid")
        except jwt.PyJWKError:
            raise InvalidField("JWT is invalid")

        
        if not decoded["role"] == "admin":
            raise Forbidden("Authorization JWT token is not admin")
        
        return func(*args, **kwargs)
    
    return wrapper

@requires_admin
def reset_password(data: ResetPasswordDTO):
    #TODO: make system work for multiple admins
    global admin_pass
    new_password = data["new_password"].strip()
    
    admin_pass = generate_password_hash(new_password)
    
    return {}, 200

@requires_admin
def clear_urls():
    get_urls.main()
    
    return {}, 200
    
@requires_admin
def download_zips():
    download_answers.main()
    
    return {}, 201