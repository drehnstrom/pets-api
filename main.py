from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify

app = Flask(__name__)
api = Api(app)

PETS = {
  '1': {'name': 'Noir', 'breed': 'Schnoodle'},
  '2': {'name': 'Bree', 'breed': 'Mutt'},
  '3': {'name': 'Gigi', 'breed': 'Retriever'},
  '4': {'name': 'Gretyl', 'breed': 'Shepherd'},
  '5': {'name': 'Rusty', 'breed': 'Poodle'},
  '6': {'name': 'Duchess', 'breed': 'Terrier'},
  '7': {'name': 'Sparky', 'breed': 'Mutt'},
}


class PetsList(Resource):
    def get(self):
        return PETS

    def post(self):
        data = request.get_json(True)
        pet_id = int(max(PETS.keys())) + 1
        pet_id = '%i' % pet_id
        PETS[pet_id] = {
            "name": data["name"],
            "breed": data["breed"],
        }
        return PETS[pet_id], 201


class Pet(Resource):
    def get(self, pet_id):
        if pet_id not in PETS:
            return "Record not found", 404
        else:
            return PETS[pet_id]

    def patch(self, pet_id):
        data = request.get_json(True)
        if pet_id not in PETS:
            return "Record not found", 404
        else:
            pet = PETS[pet_id]
            if "name" in data:
                pet["name"] = data["name"]
            if "breed" in data:
                pet["breed"] = data["breed"]
            return pet, 200

    def delete(self, pet_id):
        if pet_id not in PETS:
            return "Record not found", 404
        else:
            del PETS[pet_id]
            return '', 204


api.add_resource(PetsList, '/pets')
api.add_resource(Pet, '/pets/<pet_id>')


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)