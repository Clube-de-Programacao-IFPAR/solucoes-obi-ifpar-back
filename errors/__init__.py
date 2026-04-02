from flask import Flask
from .missing_field import MissingField, missing_field
from .invalid_field import InvalidField, invalid_field
from .unauthorized import Unauthorized, unauthorized
from .forbidden import Forbidden, forbidden
from .content_not_found import ContentNotFound, content_not_found
from .not_implemented import NotSupported, not_supported

def register_error_handlers(app: Flask):
    app.register_error_handler(MissingField, missing_field)
    app.register_error_handler(InvalidField, invalid_field)
    app.register_error_handler(Unauthorized, unauthorized)
    app.register_error_handler(Forbidden, forbidden)
    app.register_error_handler(ContentNotFound, content_not_found)
    app.register_error_handler(NotSupported, not_supported)