#src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .controllers.TodoController import todo_api
from .controllers.MTGController import mtg_api


def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(todo_api, url_prefix='/api/v1/todos')
  app.register_blueprint(mtg_api, url_prefix='/api/v1/mtg/cards')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Welcome to Python Flask Microservice API'

  return app

