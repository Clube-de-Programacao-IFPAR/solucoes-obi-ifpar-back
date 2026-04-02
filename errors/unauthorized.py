from flask import jsonify

class Unauthorized(Exception):
    status_code = 401
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def unauthorized(e: Unauthorized):
    return jsonify(e.to_dict()), e.status_code