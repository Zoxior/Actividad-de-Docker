from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

app.config["MONGO_URI"] = "mongodb://db:27017/biblioteca"
mongo = PyMongo(app)

@app.route('/libros', methods=['POST', 'GET'])
def handle_books():
    if request.method == 'POST':
        data = request.json
        mongo.db.libros.insert_one(data)
        return jsonify({'message': 'Libro añadido a la base de datos'}), 201
    
    elif request.method == 'GET':
        libros = mongo.db.libros.find()
        response = []
        if mongo.db.libros.count_documents({}) == 0:
            return jsonify('No hay libros aún.'), 200
        
        for libro in libros:
            libro['_id'] = str(libro['_id'])
            response.append(libro)
        return jsonify(response), 200


@app.route('/libros/<id>', methods=['DELETE'])
def delete_book(id):
    print('pasa por aqui la request')
    mongo.db.libros.delete_one({'_id': id})
    return jsonify({'message': 'Libro eliminado de la base de datos'}), 200
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
