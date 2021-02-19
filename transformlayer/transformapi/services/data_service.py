from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections

class Data_Service:
    __fact_services_hierarchy:DataFrame = None
    __fact_services_geography:DataFrame = None

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
        if params["Scope"]["scope_type"] == "hierarchy":
            if cls.__fact_services_hierarchy is None:
                cls.__fact_services_hierarchy = cls.__get_fact_services(params)
            
            return cls.__fact_services_hierarchy
        elif params["Scope"]["scope_type"] == "geography":
            if cls.__fact_services_geography is None:
                cls.__fact_services_geography = cls.__get_fact_services(params)
            
            return cls.__fact_services_geography

    ## returns DataFrame for a specific data definition
    @classmethod
    def get_data_for_definition(cls,id, params):
        func = cls.data_def_function_switcher.get(id, cls.get_data_def_error)
        return func(params, cls.fact_services(params))

    ## retrieves fact_services
    @classmethod
    def __get_fact_services(cls,params):
        conn = connections['default']

        table1 = ""
        left1 = right1 = ""

        if params["Scope"]["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif params["Scope"]["scope_type"] == "geography":
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
        where_stmt += (" AND t1.{} = {}".format(params["Scope"]["scope_field"],
                                    params["Scope"]["scope_field_value"]) )

        start_date = cls.__date_str_to_int(params["Scope"]["startDate"])
        end_date = cls.__date_str_to_int(params["Scope"]["endDate"])
        where_date = " AND fs.date >= {} AND fs.date <= {}".format(start_date,end_date)
        where_stmt += where_date
        
        query = query.format(t1 = table1, left1 = left1, right1 = right1)
        query += where_stmt
        
        ct = params["Scope"].get("control_type_field")
        ct_value = params["Scope"].get("control_type_value")

        query_control = """SELECT id, {} FROM dim_service_types""".format(ct)

        services = pd.read_sql(query, conn)
        service_types = pd.read_sql(query_control, conn)
        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services

    @staticmethod
    def __date_str_to_int(date):
        dt = parser.parse(date,dayfirst = False)
        date_int = (10000*dt.year)+ (100 * dt.month) + dt.day 
        return date_int

    ## DataFrame to fulfill Data Definitions 1, 7, 19
    ####    Returns: services
    ####        services - fact service data table
    def __get_services(params, services:DataFrame):
        return services
    
    ## DataFrame to fulfill Data Definition 2
    ####    Returns: services
    ####        families - unduplicated families data table
    def __get_undup_hh(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services.drop_duplicates(subset = 'research_family_key', inplace = False)
    
    ## DataFrame to fulfill Data Definiton 3
    ####    Returns: services
    ####        inidividuals - unduplicated individuals data table
    def __get_undup_indv(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services.drop_duplicates(subset = 'research_member_key', inplace = False)
    
    ## DataFrames to fulfill Data Definiton 4
    ####    Returns: (services, families)
    ####        services - fact service data table
    ####        families - unduplicated families data table
    def __get_services_and_uhh(params, services:DataFrame):
        return Data_Service.__get_services(params, services), Data_Service.__get_undup_hh(params, services)
    
    ## DataFrame to fulfill Data Definitions 5, 14, 16, 17
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children > 0
    def __get_wminor(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services[services['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 6
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children == 0
    def __get_wominor(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services[services['served_children']==0]
    
    ## DataFrame to fulfill Data Definitions 8, 18, 22
    ####    Returns: sen_hh_wminor
    ####        sen_hh_wminor - fact service data table, filtered on served_children > 0 and served_seniors > 0
    def __get_sen_wminor(params, services:DataFrame):
        seniors = Data_Service.__get_sen(params, services)
        return seniors[seniors['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 9
    ####    Returns: sen_hh_wominor
    ####        sen_hh_wominor - fact service data table, filtered on served_children == 0 and served_seniors > 0
    def __get_sen_wominor(params, services:DataFrame):
        seniors = Data_Service.__get_sen(params, services)
        return seniors[seniors['served_children']==0]
    
    ## DataFrame to fulfill Data Definitions 10, 20
    ####    Returns: sen_hh
    ####        sen_hh - fact service data table, filtered on served_seniors > 0
    def __get_sen(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services[services['served_seniors']>0]
    
    ## DataFrame to fulfill Data Definition 11
    ####    Returns: adult_hh_wminor
    ####        adult_hh_wminor - fact service data table, filtered on served_children > 0 and served_adults > 0
    def __get_adult_wminor(params, services:DataFrame):
        adults = Data_Service.__get_adult(params, services)
        return adults[adults['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 12
    ####    Returns: adult_hh_wominor
    ####        adult_hh_wominor - fact service data table, filtered on served_children == 0 and served_adults > 0
    def __get_adult_wominor(params, services:DataFrame):
        adults = Data_Service.__get_adult(params, services)
        return adults[adults['served_children']==0]
    
    ## DataFrame to fulfill Data Definition 13
    ####    Returns: adult_hh
    ####        adult_hh - fact service data table, filtered on served_adults > 0
    def __get_adult(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services[services['served_adults']>0]
    
    ## DataFrame to fulfill Data Definition 15
    ####    Returns: empty
    ####        empty - empty data table (no such thing as children wo minors)
    def __get_child_wominor(params, services:DataFrame):
        return DataFrame()
    
    ## DataFrame to fulfill Data Definition 21
    ####    Returns services_wosenior
    ####        services_wosenior - fact service data table, filtered on served_serniors == 0
    def __get_wosenior(params, services:DataFrame):
        services = Data_Service.__get_services(params, services)
        return services[services['served_seniors']==0]

    ## error, none
    def get_data_def_error(params, services:DataFrame):
        return DataFrame()

    ## Data Defintion Switcher
    # usage:
    #   func = __switcher.get(id)
    #   func()
    data_def_function_switcher = {
            1: __get_services,
            2: __get_undup_hh,
            3: __get_undup_indv,
            4: __get_services_and_uhh,
            5: __get_wminor,
            6: __get_wominor,
            7: __get_services,
            8: __get_sen_wminor,
            9: __get_sen_wominor,
            10: __get_sen,
            11: __get_adult_wminor,
            12: __get_adult_wominor,
            13: __get_adult,
            14: __get_wminor,
            15: __get_child_wominor,
            16: __get_wminor,
            17: __get_wminor,
            18: __get_wominor,
            19: __get_services,
            20: __get_sen,
            21: __get_wosenior,
            22: __get_sen_wminor,
        }

