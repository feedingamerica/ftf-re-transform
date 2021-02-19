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
    # Setting the scope type
    scope_field = input_dict["Scope"]["scope_field"]
    if scope_field.startswith("fip"):
        input_dict["Scope"]["scope_type"] = "geography"
    else:
        input_dict["Scope"]["scope_type"] = "hierarchy"
    
    # Setting the control type
    if "control_type_field" not in input_dict["Scope"]:
        input_dict["Scope"]["control_type_field"] = "dummy_is_grocery_service"

    # Setting the control type value
    if "control_type_value" not in input_dict["Scope"]:
        input_dict["Scope"]["control_type_value"] = 1


    return input_dict

def main():
    print("Beginning test function.")
    clean_dict = parse_request(sample_dict)
    print("Parsing complete.")
    print("Parsed dictionary:")
    print(str(clean_dict))
    print("Ending test function.")

if __name__=="__main__":
    main()