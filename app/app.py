from flask import Flask
from routes.client_routes import client_bp

app = Flask(__name__)
app.secret_key = "secret"

app.register_blueprint(client_bp)

if __name__ == "__main__":
    app.run(debug=True)