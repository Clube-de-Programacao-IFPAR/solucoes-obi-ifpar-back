from flask import Blueprint
from ..services.navigation_services import nav_years, nav_phases, nav_levels, nav_problems, nav_problem

nav_BP = Blueprint("nav", __name__, url_prefix="/nav")

@nav_BP.route("/years", methods=["GET"])
def get_years():
    return nav_years()

@nav_BP.route("/years/<string:year>/phases", methods=["GET"])
def get_phases(year: str):
    return nav_phases(year)

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels", methods=["GET"])
def get_levels(year: str, phase: str):
    return nav_levels(year, phase)

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems", methods=["GET"])
def get_problems(year: str, phase: str, level: str):
    return nav_problems(year, phase, level)
    
@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems/<string:problem>", methods=["GET"])
def get_specificProblem(year: str, phase: str, level: str, problem: str):
    return nav_problem(year, phase, level, problem)
