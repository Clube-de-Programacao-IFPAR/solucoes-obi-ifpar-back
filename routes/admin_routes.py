from flask import request, Blueprint 
from ..services import admin_services

admin_BP = Blueprint("admin", __name__, url_prefix="/admin")

@admin_BP.route("/login", methods=["POST"])
def login():
    data, status = admin_services.login(request.get_json())
    return data, status

@admin_BP.route("/reset_password", methods=["POST"])
def reset_password():
    data, status = admin_services.reset_password(request.get_json())
    return data, status

@admin_BP.route("/clear_urls", methods=["POST"])
def clear_urls():
    data, status = admin_services.clear_urls()
    return data, status

@admin_BP.route("download_zips", methods=["POST"])
def download_zips():
    data, status = admin_services.download_zips()
    return data, status