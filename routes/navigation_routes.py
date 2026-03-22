from flask import Blueprint
from ..services.navigation_services import nav_years, nav_phases, nav_levels, nav_problems

nav_BP = Blueprint("nav", __name__, url_prefix="/nav")

@nav_BP.route("/years", methods=["GET"])
def get_years():
    data = nav_years()
    return data

@nav_BP.route("/years/<string:year>/phases", methods=["GET"])
def get_phases(year):
    data = nav_phases(year)
    return data

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels", methods=["GET"])
def get_levels(year, phase):
    data = nav_levels(year, phase)
    return data

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems", methods=["GET"])
def get_problems(year: str, phase: str, level: str):
    data = nav_problems(year, phase, level)
    return data

