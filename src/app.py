from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__)

    from routes.portfolio import portfolio_bp
    from routes.api import api_bp

    app.register_blueprint(portfolio_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # SERVE IL MANIFEST DALLA CARTELLA /src
    @app.route('/manifest.json')
    def manifest():
        return send_from_directory(app.root_path, 'manifest.json')

    return app