# src/models/TodoModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class TodoModel(db.Model):
  """
  Todo Model
  """

  __tablename__ = 'cards'

  name = db.Column(db.String(128), primary_key=True)
  cardset = db.Column(db.String(128))
  color = db.Column(db.String(128))
  # identity = db.Column(db.String(128))
  # __tablename__ = 'todos'

  # id = db.Column(db.Integer, primary_key=True)
  # title = db.Column(db.String(128), nullable=False)
  # contents = db.Column(db.Text, nullable=False)
  # created_at = db.Column(db.DateTime)
  # modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
    self.cardset = data.get('cardset')
    self.color = data.get('color')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_todos(all_args):
    if 'title' in all_args:
      return TodoModel.query.filter(TodoModel.title == all_args.get('title'))
    return TodoModel.query.all()
  
  @staticmethod
  def get_one_todo(id):
    return TodoModel.query.get(id)

  def __repr__(self):
    return '{0},{1},{2}'.format(self.name, self.cardset, self.color)

class TodoSchema(Schema):
  """
  Todo Schema
  """
  
  name = fields.Str(dump_only=True)
  cardset = fields.Str(required=True)
  color = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
