from app import app
from app.routes.user_routes import user

app.register_blueprint(user, url_prefix='/user')