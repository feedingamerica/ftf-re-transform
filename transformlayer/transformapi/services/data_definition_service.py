from pandas.core.frame import DataFrame

class Data_Definition_Service:
    ## DataFrame to fulfill Data Definitions 1, 7, 19
    ####    Returns: services
    ####        services - fact service data table
    def __get_services(params, services:DataFrame, service_types:DataFrame):
        ct = params["scope"].get("control_type")
        ct_value = params["scope"].get("control_type_value")
        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services
    
    ## DataFrame to fulfill Data Definition 2
    ####    Returns: services
    ####        families - unduplicated families data table
    def __get_undup_hh(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services.drop_duplicates(subset = 'research_family_key', inplace = False)
    
    ## DataFrame to fulfill Data Definiton 3
    ####    Returns: services
    ####        inidividuals - unduplicated individuals data table
    def __get_undup_indv(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services.drop_duplicates(subset = 'research_member_key', inplace = False)
    
    ## DataFrames to fulfill Data Definiton 4
    ####    Returns: (services, families)
    ####        services - fact service data table
    ####        families - unduplicated families data table
    def __get_services_and_uhh(params, services:DataFrame, service_types:DataFrame):
        return Data_Definition_Service.__get_services(params, services, service_types), Data_Definition_Service.__get_undup_hh(params, services, service_types)
    
    ## DataFrame to fulfill Data Definitions 5, 14, 16, 17
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children > 0
    def __get_wminor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services[services['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 6
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children == 0
    def __get_wominor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services[services['served_children']==0]
    
    ## DataFrame to fulfill Data Definitions 8, 18, 22
    ####    Returns: sen_hh_wminor
    ####        sen_hh_wminor - fact service data table, filtered on served_children > 0 and served_seniors > 0
    def __get_sen_wminor(params, services:DataFrame, service_types:DataFrame):
        seniors = Data_Definition_Service.__get_sen(params, services, service_types)
        return seniors[seniors['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 9
    ####    Returns: sen_hh_wominor
    ####        sen_hh_wominor - fact service data table, filtered on served_children == 0 and served_seniors > 0
    def __get_sen_wominor(params, services:DataFrame, service_types:DataFrame):
        seniors = Data_Definition_Service.__get_sen(params, services, service_types)
        return seniors[seniors['served_children']==0]
    
    ## DataFrame to fulfill Data Definitions 10, 20
    ####    Returns: sen_hh
    ####        sen_hh - fact service data table, filtered on served_seniors > 0
    def __get_sen(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services[services['served_seniors']>0]
    
    ## DataFrame to fulfill Data Definition 11
    ####    Returns: adult_hh_wminor
    ####        adult_hh_wminor - fact service data table, filtered on served_children > 0 and served_adults > 0
    def __get_adult_wminor(params, services:DataFrame, service_types:DataFrame):
        adults = Data_Definition_Service.__get_adult(params, services, service_types)
        return adults[adults['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 12
    ####    Returns: adult_hh_wominor
    ####        adult_hh_wominor - fact service data table, filtered on served_children == 0 and served_adults > 0
    def __get_adult_wominor(params, services:DataFrame, service_types:DataFrame):
        adults = Data_Definition_Service.__get_adult(params, services, service_types)
        return adults[adults['served_children']==0]
    
    ## DataFrame to fulfill Data Definition 13
    ####    Returns: adult_hh
    ####        adult_hh - fact service data table, filtered on served_adults > 0
    def __get_adult(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services[services['served_adults']>0]
    
    ## DataFrame to fulfill Data Definition 15
    ####    Returns: empty
    ####        empty - empty data table (no such thing as children wo minors)
    def __get_child_wominor(params, services:DataFrame, service_types:DataFrame):
        return DataFrame()
    
    ## DataFrame to fulfill Data Definition 21
    ####    Returns services_wosenior
    ####        services_wosenior - fact service data table, filtered on served_serniors == 0
    def __get_wosenior(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services(params, services, service_types)
        return services[services['served_seniors']==0]

    ## error, none
    def get_data_def_error(params, services:DataFrame, service_types:DataFrame):
        return "get_data_def_error"

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
