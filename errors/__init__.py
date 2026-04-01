from flask import Flask
from .missing_field import MissingField, missing_field
from .invalid_field import InvalidField, invalid_field

def register_error_handlers(app: Flask):
    app.register_error_handler(MissingField, missing_field)
    app.register_error_handler(InvalidField, invalid_field)
    