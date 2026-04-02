from flask import request
import jwt
from ..scripts import get_urls
from ..scripts import download_answers
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ..dtos.login_dto import LoginDTO
from ..dtos.auth_dto import AuthDTO
from ..dtos.reset_password_dto import ResetPasswordDTO

JWT_SECRET_KEY = "Super Secret Key For JWTs by Clube de Programação IFPAR"

# default for now just for testing
admin_user = "admin"
admin_pass = generate_password_hash("admin")

jwt_count = 0

def is_admin(username, password):
    if username == admin_user and check_password_hash(admin_pass, password):
        return True


def login(data: LoginDTO):
    global jwt_count
    # returns a new token that authorizes admin for the given username and password
    # match username and password with the ones stored in the global variables
    username = data["username"]
    password = data["password"]
    
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
        return {}, 401


def requires_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #TODO: add an error message to the thingies
        auth_header = request.headers.get('Authorization', type=str)
        if not auth_header:
            return {}, 401
        parts = auth_header.split() # should be: ['Bearer', jwt]
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {}, 401
        
        token = parts[1]
        
        decoded: AuthDTO = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=["HS256"], verify=True)
        
        if not decoded["role"] == "admin":
            return {}, 401
        
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