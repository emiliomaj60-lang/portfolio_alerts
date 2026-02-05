from flask import Flask

def create_app():
    app = Flask(__name__)

    from src.routes.portfolio import portfolio_bp
    from src.routes.api import api_bp

    app.register_blueprint(portfolio_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app