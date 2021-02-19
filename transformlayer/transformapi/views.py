from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from .library import parse_request
from .services.data_service import Data_Service
from . import calculations as calc
#from .calculations import get_services_total

def test_endpoint_1(request):
    return HttpResponse('This is a test. Hello World!')

def test_endpoint_2(request):
    sample_dict = {
        "Scope": {
            "startDate":"01/01/2019",
            "endDate":"12/31/2019",
            "scope_field":"fb_id",
            "scope_field_value":21,
            "control_type_field":"dummy_is_grocery_service",
            "control_type_value":1
        },
        "ReportInfo": [
            {
                "reportId":1,
                "reportDictId":1,
                "dataDefId":1,
                "name":"services_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":1,
                "dataDefId":2,
                "name":"undup_hh_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":1,
                "dataDefId":3,
                "name":"undup_indv_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":1,
                "dataDefId":4,
                "name":"services_per_uhh_avg",
                "dataDefType":"type1"
            },
            {
                "reportId":3,
                "reportDictId":3,
                "dataDefId":3,
                "name":"name_three",
                "dataDefType":"type1"
            }
        ]
    }
    params = parse_request(sample_dict)
    num_services = calc.get_services_total(params)
    num_families = calc.get_undup_hh_total(params)

    response = "Number of unduplicated services " + str(num_services)
    response += "\n"
    response += "Number of unduplicated families " + str(num_families)
    
    print(response)
    return HttpResponse(response)

def test_data_service(request, id):
    sample_dict = {
        "Scope": {
            "startDate":"01/01/2019",
            "endDate":"12/31/2019",
            "scope_field":"fb_id",
            "scope_field_value":21,
            "control_type_field":"dummy_is_grocery_service",
            "control_type_value":1
        },
        "ReportInfo": [
            {
                "reportId":1,
                "reportDictId":1,
                "dataDefId":1,
                "name":"name_one",
                "dataDefType":"type1"
            },
            {
                "reportId":2,
                "reportDictId":2,
                "dataDefId":2,
                "name":"name_two",
                "dataDefType":"type1"
            },
            {
                "reportId":3,
                "reportDictId":3,
                "dataDefId":3,
                "name":"name_three",
                "dataDefType":"type1"
            }
        ]
    }
    params = parse_request(sample_dict)

    data = Data_Service.get_data_for_definition(id, params)
    print(data)
    return HttpResponse(str(id) + "\t" + str(data))
