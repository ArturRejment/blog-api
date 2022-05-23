from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.response import Response
from rest_framework.decorators import api_view

if TYPE_CHECKING:
	from django.http.request import HttpRequest


@api_view(['GET'])
def index(request: HttpRequest) -> Response:
	return Response({'Blog Api'})
