from django.http import JsonResponse
from django.core import serializers

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, data, **response_kwargs):
        return JsonResponse(
            data,
            **response_kwargs
        )