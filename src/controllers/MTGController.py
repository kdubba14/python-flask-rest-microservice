#/src/controllers/TodoController.py
from flask import request, g, Blueprint, json, Response
from ..models.MTGModel import MTGModel, MTGSchema
import requests
import threading

mtg_api = Blueprint('mtg_api', __name__)
mtg_schema = MTGSchema()

total_to_create = []
create_counter = 0
create_should_break = False


@mtg_api.route('/', methods=['POST'])
def create():
  """
  Create a MTG Card
  """
  req_data = request.get_json()
  data, error = mtg_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  post = MTGModel(data)
  post.save()
  data = mtg_schema.dump(post).data
  return custom_response(data, 201)

@mtg_api.route('/', methods=['GET'])
def get_all():
  """
  Get All MTG Cards
  """
  all_args = request.args
  cards = MTGModel.get_all_cards(all_args)
  return custom_response(cards, 200)

@mtg_api.route('/create', methods=['GET'])
def create_all():
  # total = []
  global total_to_create
  global create_counter
  global create_should_break

  def get_data(counter):
    global total_to_create
    global create_counter
    global create_should_break

    r  = requests.get('https://api.scryfall.com/cards?page=' + str(counter))
    print('Fetching cards from ========', 'https://api.scryfall.com/cards?page=' + str(counter))
    res = r.json()
    res_data = res['data']
    total_to_create = total_to_create + res_data

    if isinstance(res_data, list):
      if len(res_data) == 0:
        create_should_break = True
    else:
      print('AN ERROR OCCURRED --- BAD RESPONSE', res_data)
      create_should_break = True

  while True:
    threads = []

    if create_should_break == True:
      break

    for i in range(10):
      t = threading.Thread(target=get_data, args=[(i+1)+(create_counter*10)])
      t.start()
      threads.append(t)

    create_counter += 1

    for thread in threads:
      thread.join()

    print(f'%%%%%%%%%% HERES TOTAL LENGTH {len(total_to_create)} %%%%%%%%%%%')

  card_obj = {'cards': total_to_create}

  MTGModel(card_obj).create(card_obj)
  return custom_response('SUCCESS', 200)

# @mtg_api.route('/<int:todo_id>', methods=['GET'])
# def get_one(todo_id):
#   """
#   Get A Todo
#   """
  # post = TodoModel.get_one_todo(todo_id)
  # if not post:
  #   return custom_response({'error': 'post not found'}, 404)
  # data = todo_schema.dump(post).data
#   return custom_response("get one", 200)
  

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
