from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(("GET",))
def hello_world_view(request):
    return Response(data="Hello, world!")
