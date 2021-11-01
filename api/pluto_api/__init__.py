from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from pluto_api.views import routes

# create flask app
app = Flask(__name__)

# enable an open CORS Policy
cors = CORS(app, resources={r"*": {"origins": "*"}})
# create flask rest api
api = Api(app)

# add restful endpoint
api.add_resource(routes.RenderTemplate, "/template/render")
