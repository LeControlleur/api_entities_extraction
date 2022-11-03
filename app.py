from flask import Flask, jsonify, request
from flask_restful import Resource, Api

import os
import sys
sys.path.append(os.path.join(os.getcwd()))

from utils.entities_extraction import entities_extraction
from utils.statistics_analysis import database_creation, tables_creation, stats_computation

app = Flask(__name__)
api = Api(app)


class Root(Resource):
    # @app.route("/", methods=["POST"])
    def post(self):
        return {}, 204



class EntitiesExtraction(Resource):

    def post(self):
        print(request)
        body = request.json
        try :
            print(body)
            text = body['content']
            res = entities_extraction(text)
            return {"content": res}, 200
        except KeyError as e:
            return {"message": "Empty request or bad arguments"}, 400


class Stats(Resource):

    def get(self):
        try :
            res = stats_computation()
            return {"content": res}, 200
        except KeyError as e:
            return {"message": "Error while getting stats"}, 500



api.add_resource(Root, '/')
api.add_resource(EntitiesExtraction, '/api')
api.add_resource(Stats, '/stats')


database_creation()
tables_creation()

if __name__ == "__main__":
    app.run()