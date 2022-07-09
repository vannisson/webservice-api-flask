import json, os
from flask import Flask, request, Response

app = Flask(__name__)

movies = [
  {'id': 1,'name':'Scream','year':1996},
  {'id': 2,'name':'A Nightmare on Elm Street','year':1984},
  {'id': 3,'name':'Hellraiser','year':1987}
]

@app.route('/movies', methods=['GET'])
def get_all_movies():
  movies_out = json.dumps(movies)
  return movies_out, 200

@app.route('/movies/<int:idMovie>', methods=['GET'])
def get_single_movie(idMovie):
  for obj in movies: 
    if obj['id'] == idMovie:
      result = json.dumps(obj)
      return result, 200
  return Response(status=404)

@app.route('/movies', methods=['POST'])
def add_new_movie():
    if not request.json:
      Response(status=400)
    new_movie = {
    'id': movies[-1]['id'] + 1,
    'name': request.json['name'],
    'year': request.json['year']
    }
    movies.append(new_movie)
    movie_out = json.dumps(new_movie)
    return movie_out

@app.route('/movies/<int:idMovie>', methods=['PUT'])
def update_movie(idMovie): 
  if validate_req(request.json) == False:
    return Response(status=400) 
  for obj in movies: 
    if obj['id'] == idMovie:
      obj['name'] = request.json['name']
      obj['year'] = request.json['year']
      result = json.dumps(obj)
      return result, 200
  return Response(status=404)

@app.route('/movies/<int:idMovie>', methods=['DELETE'])
def delete_movie(idMovie):
    for obj in movies: 
      if obj['id'] == idMovie:
        del movies[idMovie]
        return Response(status=204)
    return Response(status=404)

# Extra
@app.route('/files', methods=['GET'])
def get_files():
  values = []
  for root, dirs, files in os.walk('.'):
    for nome in files:
      file = {}
      file['name'] = nome
      file['path'] = root
      values.append(file)
    return json.dumps({'files': values}), 200


def validate_req(JSONrequest):
  if not JSONrequest:
    return False
  if 'name' in JSONrequest and type(JSONrequest['name']) != str:
    return False
  if 'year' in JSONrequest and type(JSONrequest['year']) != int:
    return False
  return True

if __name__ == '__main__':
    app.run()

    