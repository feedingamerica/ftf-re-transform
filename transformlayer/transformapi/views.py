from django.shortcuts import render
from django.http import HttpResponse
from .library import parse_request

def test_endpoint_1(request):
    return HttpResponse('This is a test. Hello World!')

def test_endpoint_2(request):
    return HttpResponse('We are FTF.')
