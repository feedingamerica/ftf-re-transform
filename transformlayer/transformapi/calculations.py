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

#TODO deal with missing values in params ie no date to scope on.
def construct_fs_query(params):
    table1 = ""
    left1 = right1 = ""
    

    if params["scope"]["scope_type"] == "hierarchy":
        table1 = "dim_hierarchies"
        left1 = right1 = "hierarchy_id"
    elif params["scope"]["scope_type"] == "geography":
        table1 = "dim_geos"
        left1 = "dimgeo_id"
        right1 = "id"

    query = """SELECT fs.research_service_key, fs.{left1}, fs.service_status, fs.service_id,
    fs.research_family_key, fs.research_member_key
    FROM fact_services AS fs
    LEFT JOIN {t1} AS t1 ON fs.{left1} = t1.{right1}
    LEFT JOIN dim_service_statuses ON fs.service_status = dim_service_statuses.status 
    """
    where_stmt = "WHERE fs.service_status = 17"
    where_stmt += (" AND t1.{} = {}".format(params["scope"]["scope_field"], 
                                params["scope"]["scope_field_value"]) )

    start_date = date_str_to_int(params["scope"]["start_date"])
    end_date = date_str_to_int(params["scope"]["end_date"])
    where_date = " AND fs.date >= {} AND fs.date <= {}".format(start_date,end_date)
    where_stmt += where_date
    
    query = query.format(t1 = table1, left1 = left1, right1 = right1)
    query += where_stmt
    return query

def date_str_to_int(date):
    dt = parser.parse(date,dayfirst = False)
    date_int = (10000*dt.year)+ (100 * dt.month) + dt.day 
    return date_int



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

    query_fact_services = construct_fs_query(params)
    print(query_fact_services)
    ct = params["scope"].get("control_type")
    ct_value = params["scope"].get("control_type_value")

    query_control = """SELECT id, {} FROM dim_service_types""".format(ct)

    #TODO replace with calls to christina's service
    services = pd.read_sql(query_fact_services,connection)
    service_types = pd.read_sql(query_control, connection)

    services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
    services = services.query('{} == {}'.format(ct, ct_value))
    return (len(services), services)

#data def 2
def get_undup_hh_total(connection,params,scoped_services = None):
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
    if scoped_services is None:
        services = get_services_total(connection, params)[1]
    else:
        services = scoped_services
    
    unique_families = services.drop_duplicates(subset = 'research_family_key', inplace = False)
    return (len(unique_families), unique_families)


def main():
    print(date_str_to_int("6/16/1998"))

if __name__=="__main__":
    main()

