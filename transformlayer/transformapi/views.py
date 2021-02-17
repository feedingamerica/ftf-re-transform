from django.shortcuts import render
from django.http import HttpResponse
from .library import parse_request
from .services.data_service import Data_Service

def test_endpoint_1(request):
    return HttpResponse('This is a test. Hello World!')

def test_endpoint_2(request):
    return HttpResponse('We are FTF.')

def test_data_service(request, id):
    return HttpResponse(Data_Service.get_data_from_definition(id))
