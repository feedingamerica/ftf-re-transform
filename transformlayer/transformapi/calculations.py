from .services.data_service import Data_Service as ds

BIG_NUM_NAMES = ["services_total", "undup_hh_total", "undup_indv_total", "services_per_uhh_avg"]
DEFAULT_CTRL = "dummy_is_grocery_service"
DEFAULT_CTRL_VAL = "1"
    
#3
def get_undup_indv_total(params):
    pass
#4
def get_services_per_uhh_avg(params):
    pass

#data def 1
def get_services_total(params):
    """Calculate number of services. DataDef 1

    Arguments:
    params - a dictionary of values to scope the queries

    Returns: num_services
    num_services - number of unduplicated services

    """
    #TODO replace with calls to christina's service
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

def main():
    print(ds.date_str_to_int("6/16/1998"))

if __name__=="__main__":
    main()

