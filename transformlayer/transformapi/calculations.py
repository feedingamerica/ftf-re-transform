from .services.data_service import Data_Service
import pandas as pd
import numpy as np
import dateutil.parser as parser
from .library import parse_request
from django.db import connections

BIG_NUM_NAMES = ["services_total", "undup_hh_total", "undup_indv_total", "services_per_uhh_avg"]
DEFAULT_CTRL = "dummy_is_grocery_service"
DEFAULT_CTRL_VAL = "1"
    
#3
def get_undup_indv_total(connection, params):
    pass
#4
def get_services_per_uhh_avg(connection, params):
    pass

#data def 1
def get_services_total(connection, params):
    """Calculate number of services. DataDef 1

    Arguments:
    connection - a MySQLConnection object or equivalent that can work with pandas.read_sql
    params - a dictionary of values to scope the queries

    Returns: (num_services, services)
    num_services - number of unduplicated services
    services - pandas dataframe of the services

    Columns always in services:
    research_service_key
    service_status
    service_id
    research_family_key
    research_member_key
    Additional columns depending on params:
    hierarchy_id - if scope_type is "hierarchy"
    dimgeo_id - if scope_type is "geography"

    """
    #TODO replace with calls to christina's service
    return len(Data_Service.get_data_for_definition(1, connection, params))

#data def 2
def get_undup_hh_total(connection,params):
    """Calculate number of unique families. DataDef 2

    Arguments:
    connection - a MySQLConnection object or equivalent that can work with pandas.read_sql
    params - a dictionary of values to scope the queries
    scoped_services - pandas dataframe obtained from call to get_services_total

    Requires:
    if scoped_services is not None then it should have a column named 'research_family_key'

    Modifies:
    Nothing

    Returns: (num_familes, services)
    num_services - number of unique families
    services - pandas dataframe of the families

    Columns always in families:
    research_service_key
    service_status
    service_id
    research_family_key
    research_member_key
    Additional columns depending on params:
    hierarchy_id - if scope_type is "hierarchy"
    dimgeo_id - if scope_type is "geography"

    """
    return len(Data_Service.get_data_for_definition(2, connection, params))


def main():
    print(Data_Service.date_str_to_int("6/16/1998"))

if __name__=="__main__":
    main()

