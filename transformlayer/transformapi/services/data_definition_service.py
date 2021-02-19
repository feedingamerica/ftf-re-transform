from pandas.core.frame import DataFrame

class Data_Definition_Service:
    def merge_service_types(params, services, service_types):
        ct = params["scope"].get("control_type")
        ct_value = params["scope"].get("control_type_value")
        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services

    ## Data Definition 1
    ####    Returns: services
    ####        services - fact service data table
    def __get_services_total(params, services:DataFrame, service_types:DataFrame):
        return Data_Definition_Service.merge_service_types(params, services, service_types)
    
    ## Data Definition 2
    ####    Returns: services
    ####        families - unduplicated families data table
    def __get_undup_hh_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.merge_service_types(params, services, service_types)
        return services.drop_duplicates(subset = 'research_family_key', inplace = False)
    
    ## Data Definiton 3
    ####    Returns: services
    ####        inidividuals - unduplicated individuals data table
    def __get_undup_indv_total(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.merge_service_types(params, services, service_types)
        return services.drop_duplicates(subset = 'research_member_key', inplace = False)
    
    ## Data Definiton 4
    ####    Returns: (services, families)
    ####        services - fact service data table
    ####        families - unduplicated families data table
    def __get_services_per_uhh_avg(params, services:DataFrame, service_types:DataFrame):
        return Data_Definition_Service.__get_services_total(params, services, service_types), Data_Definition_Service.__get_undup_hh_total(params, services, service_types)
    
    ## Data Definition 5
    ####    Returns: services
    ####        services - fact service data table, filtered on served_chilren > 0
    def __get_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.merge_service_types(params, services, service_types)
        return services[services['served_children']>0]
    
    ## Data Definition 6
    ####    Returns: services
    ####        services - fact service data table, filtered on served_chilren == 0
    def __get_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        services = Data_Definition_Service.merge_service_types(params, services, service_types)
        return services[services['served_children']==0]
    
    ## 7
    def __get_hh_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_total"
    
    ## 8
    def __get_indv_sen_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_sen_hh_wminor"
    
    ## 9
    def __get_indv_sen_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_sen_hh_wominor"
    
    ## 10
    def __get_indv_sen_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_sen_total"
    
    ## 11
    def __get_indv_adult_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_adult_hh_wminor"
    
    ## 12
    def __get_indv_adult_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_adult_hh_wominor"
    
    ## 13
    def __get_indv_adult_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_adult_total"
    
    ## 14
    def __get_indv_child_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_child_hh_wminor"
    
    ## 15
    def __get_indv_child_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_child_hh_wominor"
    
    ## 16
    def __get_indv_child_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_child_total"
    
    ## 17
    def __get_indv_total_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_total_hh_wminor"
    
    ## 18
    def __get_indv_total_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_total_hh_wominor"
    
    ## 19
    def __get_indv_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_total"
    
    ## 20
    def __get_hh_wsenior(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_wsenior"
    
    ## 21
    def __get_hh_wosenior(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_wosenior"
    
    ## 22
    def __get_hh_grandparent(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_grandparent"

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
            7: __get_hh_total,
            8: __get_indv_sen_hh_wminor,
            9: __get_indv_sen_hh_wominor,
            10: __get_indv_sen_total,
            11: __get_indv_adult_hh_wminor,
            12: __get_indv_adult_hh_wominor,
            13: __get_indv_adult_total,
            14: __get_indv_child_hh_wminor,
            15: __get_indv_child_hh_wominor,
            16: __get_indv_child_total,
            17: __get_indv_total_hh_wminor,
            18: __get_indv_total_hh_wominor,
            19: __get_indv_total,
            20: __get_hh_wsenior,
            21: __get_hh_wosenior,
            22: __get_hh_grandparent,
        }
