# renderers.py
from rest_framework import renderers
import json
from django.core.serializers.json import DjangoJSONEncoder

class CustomRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {
            "status": "Error" if "ErrorDetail" in str(data) else "Successful",
            "data": data
        }
        return json.dumps(response, cls=DjangoJSONEncoder)
