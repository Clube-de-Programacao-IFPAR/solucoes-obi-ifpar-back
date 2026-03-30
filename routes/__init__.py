from .questions_routes import questions_BP
from .search_routes import search_BP
from .navigation_routes import nav_BP
from .admin_routes import admin_BP

def register_routes(app):
    app.register_blueprint(questions_BP)
    app.register_blueprint(search_BP)
    app.register_blueprint(nav_BP)
    app.register_blueprint(admin_BP)