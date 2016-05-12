from flask import Flask, jsonify, request, abort, Response, send_from_directory
import json
from SHpersistence import SuperHeroStore as SHS
from SuperHeroModel import Model as SHModel

database = 'data.json'

app = Flask(__name__)
store = SHS(database)

@app.route('/html/', methods=['GET'])
@app.route('/html/<path:path>', methods=['GET'])
def static_html(path = 'index.html'):
    return send_from_directory('html', path)

@app.route('/article', methods=['GET'])
def get_heros():
    heros= []
    for hero in store.list_heros():
        heros.append({'hero': hero['name'], 'uri': '/article/' + str(hero['id'])})
    return jsonify({"heros":heros})   

@app.route('/article/<int:heroid>', methods=['GET'])
def get_hero(heroid):
    if not store.hero_exists(heroid):
        abort(404)
    return jsonify(store.read_hero(heroid))

@app.route('/article', methods=['POST'])
def create_hero():
    file = request.files['herofile']
    if not (file and file.filename.rsplit('.', 1)[1] == 'txt'):
        abort(400)
    if not request.form['dc_or_marvel'] in ['dc','marvel']:
        abort(400)
        
    id = store.create_hero(file.filename.rsplit('.', 1)[0], file.read(), request.form['dc_or_marvel'])
    return Response('Created', headers={'location':'/article/' + str(id)})

@app.route('/article/<int:heroid>', methods=['PUT'])
def update_hero(heroid):
    if not store.hero_exists(heroid):
        abort(404)
    file = request.files['herofile']
    if not (file and file.filename.rsplit('.', 1)[1] == "txt"):
        abort(400)
    if not request.form['dc_or_marvel'] in ['dc','marvel']:
        abort(400)
    store.update_hero(heroid,file.filename.rsplit('.', 1)[0], file.read(), request.form['dc_or_marvel'])
    return Response('Updated')

@app.route('/article/<int:heroid>', methods=['DELETE'])
def delete_hero(heroid):
    if not store.hero_exists(heroid):
        abort(404)
    store.delete_hero(heroid)
    return Response("Deleted")

@app.route('/train', methods=['GET'])
def train_hero_predictor():
    model = SHModel(store)
    model.train()
    return jsonify({'result': 'Model trained'})

@app.route('/predict', methods=['POST'])
def predict_universe():
    file = request.files['herofile']
    if not (file and file.filename.rsplit('.', 1)[1] == 'txt'):
        abort(400)
    model = SHModel(store)
    prediction = model.predict(file.read())
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

    
        
       