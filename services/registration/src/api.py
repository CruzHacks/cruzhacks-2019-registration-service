from flask_restful import Api, Resource

api = Api()

@api.resource('/')
class Home(Resource):
    def get(self):
        return 'Hello, World.'
