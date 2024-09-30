from app.routes.chat import chat_blueprint

def init_routes(app):
    app.register_blueprint(chat_blueprint)
