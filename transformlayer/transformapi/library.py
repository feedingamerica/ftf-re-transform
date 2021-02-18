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

def parse_request(input_dict):
    clean_dict = {
        "scope": {
            "scope_type":None,
            "scope_field":None,
            "scope_field_value":None,
            "start_date":None,
            "end_date":None,
            "control_type":None,
            "control_type_value":None
        },
        "data_dictionary": {
            "data_list":None
        }
    }

    # Setting the scope type
    scope_field = input_dict["Scope"]["scope_field"]
    if scope_field.startswith("fip"):
        clean_dict["scope"]["scope_type"] = "geography"
    else:
        clean_dict["scope"]["scope_type"] = "hierarchy"
    
    # Setting the scope field
    clean_dict["scope"]["scope_field"] = scope_field

    # Setting the scope field value 
    clean_dict["scope"]["scope_field_value"] = int(input_dict["Scope"]["scope_field_value"])

    # Setting the start date
    clean_dict["scope"]["start_date"] = input_dict["Scope"]["startDate"]
    
    # Setting the end date
    clean_dict["scope"]["end_date"] = input_dict["Scope"]["endDate"]

    # Setting the control type
    if "control_type_field" not in input_dict["Scope"]:
        clean_dict["scope"]["control_type"] = "dummy_is_grocery_service"
    else:
        clean_dict["scope"]["control_type"] = input_dict["Scope"]["control_type_field"]

    # Setting the control type value
    if "control_type_value" not in input_dict["Scope"]:
        clean_dict["scope"]["control_type_value"] = 1
    else:
        clean_dict["scope"]["control_type_value"] = int(input_dict["Scope"]["control_type_value"])

    datalist = list()

    # Getting everything from data dict 
    for item in input_dict["ReportInfo"]:
        current_object = {
            "reportDictId":None,
            "dataDefId":None,
            "name":None,
            "dataDefType":None
        }

        # Getting dataDefId
        current_object["dataDefId"] = int(item["dataDefId"])

        # Getting name
        current_object["name"] = item["name"]

        # Getting dataDefType
        current_object["dataDefType"] = item["dataDefType"]
        current_object["reportDictId"] = item["reportDictId"]

        datalist.append(current_object)
    
    clean_dict["data_dictionary"]["data_list"] = datalist

    return clean_dict

def main():
    print("Beginning test function.")
    clean_dict = parse_request(sample_dict)
    print("Parsing complete.")
    print("Parsed dictionary:")
    print(str(clean_dict))
    print("Ending test function.")

if __name__=="__main__":
    main()