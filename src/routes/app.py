from flask import Flask

# trigger redeploy

def create_app():
    app = Flask(__name__)

    from routes.portfolio import portfolio_bp
    from routes.api import api_bp



    app.register_blueprint(portfolio_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route('/manifest.json')
    def manifest():
        return send_from_directory('.', 'manifest.json')

    return app