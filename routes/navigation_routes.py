from flask import Blueprint
from ..services.navigation_services import nav_years, nav_phases, nav_levels, nav_problems, nav_problem

nav_BP = Blueprint("nav", __name__, url_prefix="/nav")

@nav_BP.route("/years", methods=["GET"])
def get_years():
    """
    :status 200: Returns list of the avaliable years stored in the server
    """
    return nav_years()

@nav_BP.route("/years/<string:year>/phases", methods=["GET"])
def get_phases(year: str):
    """
    :param string year: Year to lookup the phases for

    :status 200: Returns list of the avaliable phases for the given year stored
                 in the server as well as the year given
    :status 400: Year was invalid
    :status 404: Year was not found in server

    :>json string ano: Year provided
    :>json array fases: Array of avaliable phases
    """
    return nav_phases(year)

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels", methods=["GET"])
def get_levels(year: str, phase: str):
    """
    :param string year: Year to lookup the levels for
    :param string phase: Phase to lookup the levels for

    :status 200: Returns list of the avaliable levels for the given year and
                 phase stored in the server as well as the year and phase given
    :status 400: Year or phase was invalid
    :status 404: Year or phase was not found in server

    :>json string ano: Year provided
    :>json string fase: Phase provided
    :>json array niveis: Array of avaliable levels
    """
    return nav_levels(year, phase)

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems", methods=["GET"])
def get_problems(year: str, phase: str, level: str):
    """
    :param string year: Year to lookup the problems for
    :param string phase: Phase to lookup the problems for
    :param string level: Level to lookup the problems for

    :status 200: Returns list of the avaliable problems for the given year,
                 phase and level stored in the server as well as the year,
                 phase and level given
    :status 400: Year, phase or level was invalid
    :status 404: Year, phase or level was not found in server

    :>json string ano: Year provided
    :>json string fase: Phase provided
    :>json string nivel: Level provided
    :>json array questoes: Array of avaliable problems
    """
    return nav_problems(year, phase, level)
    
@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems/<string:problem>", methods=["GET"])
def get_specific_problem(year: str, phase: str, level: str, problem: str):
    """
    :param string year: Year to lookup the problems for
    :param string phase: Phase to lookup the problems for
    :param string level: Level to lookup the problems for
    :param string problem: Problem to lookup the problems for

    :status 200: Returns list of the avaliable problems for the given year,
                 phase, level and problem stored in the server as well as the
                 year, phase, level and problem given
    :status 400: Year, phase or level was invalid
    :status 404: Year, phase, level or problem was not found in server

    :>json string ano: Year provided
    :>json string fase: Phase provided
    :>json string nivel: Level provided
    :>json string url: Url for the answer zip stored at the obi website
    :>json boolean flag: Whether the server has the problem avaliable or not
    """
    return nav_problem(year, phase, level, problem)
