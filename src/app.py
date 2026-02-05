from flask import Flask

# trigger redeploy

def create_app():
    app = Flask(__name__)

    from routes.portfolio import portfolio_bp
    from routes.api import api_bp



    app.register_blueprint(portfolio_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app