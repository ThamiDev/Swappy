from flask import Flask
from flask_jwt_extended import JWTManager
from .models import db
from .routes import user_bp, task_bp, auth_bp

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)

