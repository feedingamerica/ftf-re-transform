from .services.data_service import Data_Service as ds

BIG_NUM_NAMES = ["services_total", "undup_hh_total", "undup_indv_total", "services_per_uhh_avg"]
DEFAULT_CTRL = "dummy_is_grocery_service"
DEFAULT_CTRL_VAL = "1"
    

#data def 1
def get_services_total(params):
    """Calculate number of services. DataDef 1

    Arguments:
    params - a dictionary of values to scope the queries

    Returns: num_services
    num_services - number of unduplicated services

    """
    return len(ds.get_data_for_definition(1, params))

#data def 2
def get_undup_hh_total(params):
    """Calculate number of unique families. DataDef 2

    Arguments:
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_familes
    num_familes - number of unique families

    """
    return len(ds.get_data_for_definition(2, params))
#data def 3
def undup_indv_total(params):
    """Calculate number of unique individuals. DataDef 3

    Arguments:
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_indv
    num_familes - number of unique individuals

    """

    return len(ds.get_data_for_definition(3, params))

#data def 4
def get_services_per_uhh_avg(params):
    """Calculate number of services per family DataDef 4

    Arguments:
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_services_avg
    num_services_avg - average number of services per family

    """
    num_services = len(ds.get_data_for_definition(1, params))
    num_families = len(ds.get_data_for_definition(2, params))
    return num_families/num_services


def main():
    print(ds.__date_str_to_int("6/16/1998"))

if __name__=="__main__":
    main()

