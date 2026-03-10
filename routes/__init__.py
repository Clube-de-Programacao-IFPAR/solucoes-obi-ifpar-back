from .questions_routes import questions_BP

def register_routes(app):
    app.register_blueprint(questions_BP)