from pandas.core.frame import DataFrame
from .data_definition_service import Data_Definition_Service as dds
import dateutil.parser as parser
import pandas as pd
from django.db import connections

class Data_Service:
    __fact_services_hierarchy:DataFrame = None
    __service_types_hierarchy:DataFrame = None
    __fact_services_geography:DataFrame = None
    __service_types_geography:DataFrame = None

    ##  getter and setter for fact_services based on the scope "hierarchy" or "geography" (also sets related service_types if None)
    ##  Columns always in services:
    ##      research_service_key
    ##      service_status
    ##      service_id
    ##      research_family_key
    ##      research_member_key
    ##      served_children
    ##      served_adults
    ##      served_seniors
    ##      served_total
    ##      Additional columns depending on params:
    ##      hierarchy_id - if scope_type is "hierarchy"
    ##      dimgeo_id - if scope_type is "geography"
    @classmethod
    def fact_services(cls,params):
        if params["scope"]["scope_type"] == "hierarchy":
            if Data_Service.__fact_services_hierarchy is None:
                Data_Service.__fact_services_hierarchy, Data_Service.__service_types_hierarchy = Data_Service.__get_fact_services(params)
            
            return Data_Service.__fact_services_hierarchy
        elif params["scope"]["scope_type"] == "geography":
            if Data_Service.__fact_services_geography is None:
                Data_Service.__fact_services_geography, Data_Service.__service_types_geography = Data_Service.__get_fact_services(params)
            
            return Data_Service.__fact_services_geography

    # getter and setter for service_types based on the scope "hierarchy" or "geography" (also sets related fact_service if None)
    @classmethod
    def service_types(cls,params):
        if params["scope"]["scope_type"] == "hierarchy":
            if Data_Service.__service_types_hierarchy is None:
                Data_Service.__fact_services_hierarchy, Data_Service.__service_types_hierarchy = Data_Service.__get_fact_services(params)
            
            return Data_Service.__service_types_hierarchy
        elif params["scope"]["scope_type"] == "geography":
            if Data_Service.__fact_services_geography is None:
                Data_Service.__fact_services_geography, Data_Service.__service_types_geography = Data_Service.__get_fact_services(params)

            return Data_Service.__service_types_geography


    ## returns DataFrame for a specific data definition
    @classmethod
    def get_data_for_definition(cls,id, params):
        func = dds.data_def_function_switcher.get(id, dds.get_data_def_error)
        return func(params, Data_Service.fact_services(params), Data_Service.service_types(params))

    ## retrieves fact_services
    @classmethod
    def __get_fact_services(cls,params):
        conn = connections['default']

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
        fs.research_family_key, fs.research_member_key, fs.served_children, fs.served_adults, fs.served_seniors, fs.served_total
        FROM fact_services AS fs
        LEFT JOIN {t1} AS t1 ON fs.{left1} = t1.{right1}
        LEFT JOIN dim_service_statuses ON fs.service_status = dim_service_statuses.status 
        """
        where_stmt = "WHERE fs.service_status = 17"
        where_stmt += (" AND t1.{} = {}".format(params["scope"]["scope_field"],
                                    params["scope"]["scope_field_value"]) )

        start_date = Data_Service.__date_str_to_int(params["scope"]["start_date"])
        end_date = Data_Service.__date_str_to_int(params["scope"]["end_date"])
        where_date = " AND fs.date >= {} AND fs.date <= {}".format(start_date,end_date)
        where_stmt += where_date
        
        query = query.format(t1 = table1, left1 = left1, right1 = right1)
        query += where_stmt
        
        ct = params["scope"].get("control_type")

        query_control = """SELECT id, {} FROM dim_service_types""".format(ct)

        services = pd.read_sql(query, conn)
        service_types = pd.read_sql(query_control, conn)

        return services, service_types

    @staticmethod
    def __date_str_to_int(date):
        dt = parser.parse(date,dayfirst = False)
        date_int = (10000*dt.year)+ (100 * dt.month) + dt.day 
        return date_int
