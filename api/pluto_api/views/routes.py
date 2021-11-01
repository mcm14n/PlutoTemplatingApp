from re import template
from flask_restful import reqparse, abort, Resource

from pluto_api import exceptions
from pluto_api.views.utils.status import CODES

from pluto_api.formatter import formatter


# initiate request parser
parser = reqparse.RequestParser()
# add accepted args from the body
parser.add_argument("template")


class RenderTemplate(Resource):
    """ Endpoint /template/render to process and render a template """

    def post(self):
        try:
            body = parser.parse_args()
            template = formatter.template_formatter(body["template"])
            resp = dict(template=template)
            return resp, CODES["CREATED"]
        except exceptions.AppError as exc:
            abort(exc.status, description=exc.message)
