#src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# db = create_engine(db_string)  
# base = declarative_base()

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .TodoModel import TodoModel, TodoSchema