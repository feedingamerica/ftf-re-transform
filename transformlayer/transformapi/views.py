from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connections
from .library import parse_request
from .services.data_service import Data_Service
from . import calculations as calc
from .calculations import CalculationDispatcher
from print_dict import print_dict, format_dict
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
    num_services = calc.__get_services_total(params)
    num_families = calc.__get_undup_hh_total(params)

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

def get_report_big_numbers(request):
    input_dict = {
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
                "reportId":2,
                "reportDictId":2,
                "dataDefId":2,
                "name":"undup_hh_total",
                "dataDefType":"type1"
            },
            {
                "reportId":3,
                "reportDictId":3,
                "dataDefId":3,
                "name":"undup_indv_total",
                "dataDefType":"type1"
            },
            {
                "reportId":4,
                "reportDictId":4,
                "dataDefId":4,
                "name":"services_per_uhh_avg",
                "dataDefType":"type1"
            }
        ]
    }

    params = parse_request(input_dict)
    cd = CalculationDispatcher(params)
    cd.run_calculations()

    context = { 'report_output': format_dict(cd.request) }
    print_dict(input_dict)
    return render(request, 'transformapi/get-report.html', context)

def get_report_ohio(request):
    input_dict = {
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
                "reportDictId":2,
                "dataDefId":5,
                "name":"hh_wminor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":6,
                "name":"hh_wominor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":7,
                "name":"hh_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":8,
                "name":"indv_sen_hh_wminor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":9,
                "name":"indv_sen_hh_wominor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":10,
                "name":"indv_sen_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":11,
                "name":"indv_adult_hh_wminor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":12,
                "name":"indv_adult_hh_wominor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":13,
                "name":"indv_adult_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":14,
                "name":"indv_child_hh_wminor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":15,
                "name":"indv_child_hh_wominor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":16,
                "name":"indv_child_total",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":17,
                "name":"indv_total_hh_wminor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":18,
                "name":"indv_total_hh_wominor",
                "dataDefType":"type1"
            },
            {
                "reportId":1,
                "reportDictId":2,
                "dataDefId":19,
                "name":"indv_total",
                "dataDefType":"type1"
            }
        ]
    }

    params = parse_request(input_dict)
    cd = CalculationDispatcher(params)
    cd.run_calculations()

    context = { 'report_output': format_dict(cd.request) }
    print_dict(input_dict)
    return render(request, 'transformapi/get-report.html', context)