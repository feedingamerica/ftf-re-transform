from pandas.core.frame import DataFrame

class Data_Definition_Service:
    ## Data Definition 1, 7, 19
    ####    Returns: services
    ####        services - fact service data table
    def __get_services_total(params, services:DataFrame, service_types:DataFrame):
        ct = params["scope"].get("control_type")
        ct_value = params["scope"].get("control_type_value")
        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services
    
    ## Data Definition 2
    ####    Returns: services
    ####        families - unduplicated families data table
    def __get_undup_hh_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services.drop_duplicates(subset = 'research_family_key', inplace = False)
    
    ## Data Definiton 3
    ####    Returns: services
    ####        inidividuals - unduplicated individuals data table
    def __get_undup_indv_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services.drop_duplicates(subset = 'research_member_key', inplace = False)
    
    ## Data Definiton 4
    ####    Returns: (services, families)
    ####        services - fact service data table
    ####        families - unduplicated families data table
    def __get_services_per_uhh_avg(params, services:DataFrame, service_types:DataFrame):
        return Data_Definition_Service.__get_services_total(params, services, service_types), Data_Definition_Service.__get_undup_hh_total(params, services, service_types)
    
    ## Data Definition 5
    ####    Returns: services
    ####        services - fact service data table, unduplicated households filtered on served_children > 0
    def __get_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services[services['served_children']>0]
    
    ## Data Definition 6
    ####    Returns: services
    ####        services - fact service data table, unduplicated households filtered on served_children == 0
    def __get_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services[services['served_children']==0]
    
    ## Data Definition 8, 22
    ####    Returns: sen_hh_wminor
    ####        sen_hh_wminor - fact service data table, filtered on served_children > 0 and served_seniors > 0
    def __get_indv_sen_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        seniors = Data_Definition_Service.__get_indv_sen_total(params, services, service_types)
        return seniors[seniors['served_children']>0]
    
    ## Data Definition 9
    ####    Returns: sen_hh_wominor
    ####        sen_hh_wominor - fact service data table, filtered on served_children == 0 and served_seniors > 0
    def __get_indv_sen_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        seniors = Data_Definition_Service.__get_indv_sen_total(params, services, service_types)
        return seniors[seniors['served_children']==0]
    
    ## Data Definition 10, 20
    ####    Returns: sen_hh
    ####        sen_hh - fact service data table, filtered on served_seniors > 0
    def __get_indv_sen_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services[services['served_seniors']>0]
    
    ## Data Definition 11
    ####    Returns: adult_hh_wminor
    ####        adult_hh_wminor - fact service data table, filtered on served_children > 0 and served_adults > 0
    def __get_indv_adult_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        adults = Data_Definition_Service.__get_indv_adult_total(params, services, service_types)
        return adults[adults['served_children']>0]
    
    ## Data Definition 12
    ####    Returns: adult_hh_wominor
    ####        adult_hh_wominor - fact service data table, filtered on served_children == 0 and served_adults > 0
    def __get_indv_adult_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        adults = Data_Definition_Service.__get_indv_adult_total(params, services, service_types)
        return adults[adults['served_children']==0]
    
    ## Data Definition 13
    ####    Returns: adult_hh
    ####        adult_hh - fact service data table, filtered on served_adults > 0
    def __get_indv_adult_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services[services['served_adults']>0]
    
    ## Data Definition 15
    ####    Returns: empty
    ####        empty - empty data table (no such thing as children wo minors)
    def __get_indv_child_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return DataFrame()
    
    ## Data Definition 14 and 16
    ####    Returns: children_hh
    ####        children_hh - fact service data table, filtered on served_children > 0
    def __get_indv_child_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services[services['served_children']>0]
    
    ## Data Definition 17
    ####    Returns services_wminor
    ####        services_wminor - fact service data table, filtered on served_children > 0
    def __get_indv_total_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_indv_total(params, services, service_types)
        return services[services['served_children']>0]
    
    ## Data Definition 18
    ####    Returns services_wominor
    ####        services_wominor - fact service data table, filtered on served_children == 0
    def __get_indv_total_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_indv_total(params, services, service_types)
        return services[services['served_children']==0]
    
    ## Data Definition 21
    ####    Returns services_wosenior
    ####        services_wosenior - fact service data table, filtered on served_serniors == 0
    def __get_hh_wosenior(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.__get_services_total(params, services, service_types)
        return services[services['served_seniors']==0]

    ## error, none
    def get_data_def_error(params, services:DataFrame, service_types:DataFrame):
        return "get_data_def_error"

    ## Data Defintion Switcher
    # usage:
    #   func = __switcher.get(id)
    #   func()
    data_def_function_switcher = {
            1: __get_services_total,
            2: __get_undup_hh_total,
            3: __get_undup_indv_total,
            4: __get_services_per_uhh_avg,
            5: __get_hh_wminor,
            6: __get_hh_wominor,
            7: __get_services_total,
            8: __get_indv_sen_hh_wminor,
            9: __get_indv_sen_hh_wominor,
            10: __get_indv_sen_total,
            11: __get_indv_adult_hh_wminor,
            12: __get_indv_adult_hh_wominor,
            13: __get_indv_adult_total,
            14: __get_indv_child_total,
            15: __get_indv_child_hh_wominor,
            16: __get_indv_child_total,
            17: __get_indv_total_hh_wminor,
            18: __get_indv_total_hh_wominor,
            19: __get_services_total,
            20: __get_indv_sen_total,
            21: __get_hh_wosenior,
            22: __get_indv_sen_hh_wminor,
        }
