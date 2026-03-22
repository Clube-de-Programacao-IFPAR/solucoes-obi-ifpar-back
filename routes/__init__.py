from .questions_routes import questions_BP
from .search_routes import search_BP

def register_routes(app):
    app.register_blueprint(questions_BP)
    app.register_blueprint(search_BP)