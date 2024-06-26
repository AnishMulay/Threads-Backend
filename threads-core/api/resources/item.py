from flask_restful import Resource
from flask import current_app as app
from flask import request, jsonify, make_response

class ItemResource(Resource):
    def post(self):
        try:
            print("INSIDE POST REQUEST")

            name = request.json.get('name')
            description = request.json.get('description')

            if not name or not description:
                raise ValueError("Name and description are required fields.")

            client = app.config['MONGO_CLIENT']
            db = client.get_database('threads')
            items_collection = db.get_collection('items')

            item = {
                'name': name,
                'description': description
            }

            result = items_collection.insert_one(item)

            if result.inserted_id:
                print("----------- ITEM INSERTED ----------")
                celery = app.config['CELERY']
                celery.send_task('celery_app.process_item', args=[str(result.inserted_id)])
                print("----------- TASK ADDED ----------")

                response_data = {
                    'message': 'Item added successfully',
                    'item_id': str(result.inserted_id)
                }
                return make_response(jsonify(response_data), 201)
            else:
                raise Exception('Failed to add item')

        except Exception as e:
            import traceback
            traceback.print_exc()
            response_data = {
                "error": str(e)
            }
            return make_response(jsonify(response_data), 500)