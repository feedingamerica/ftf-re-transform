from pandas.core.frame import DataFrame


class Data_Definition_Service:
    ## Data Definition 1
    ####    Expects:
    ####        params
    ####        services - fact service data table
    ####        service_types - service_types data table
    @staticmethod
    def __get_services_total(params, services:DataFrame, service_types:DataFrame):
        ct = params["scope"].get("control_type")
        ct_value = params["scope"].get("control_type_value")

        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services
    
    ## Data Definition 2
    ####    Expects:
    ####        services - fact service data table
    @staticmethod
    def __get_undup_hh_total(params, services:DataFrame, service_types:DataFrame):
        ct = params["scope"].get("control_type")
        ct_value = params["scope"].get("control_type_value")
        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services.drop_duplicates(subset = 'research_family_key', inplace = False)
    
    ## 3
    @staticmethod
    def __get_undup_indv_total(params, services:DataFrame, service_types:DataFrame):
        ct = params["scope"].get("control_type")
        ct_value = params["scope"].get("control_type_value")
        services = services.merge(service_types, how = 'left', left_on= 'service_id', right_on = 'id')
        services = services.query('{} == {}'.format(ct, ct_value))
        return services.drop_duplicates(subset = 'research_member_key', inplace = False)
    
    ## 4
    @staticmethod
    def __get_services_per_uhh_avg(params, services:DataFrame, service_types:DataFrame):
        return "__get_services_per_uhh_avg"
    
    ## 5
    @staticmethod
    def __get_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_wminor"
    
    ## 6
    @staticmethod
    def __get_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_wominor"
    
    ## 7
    @staticmethod
    def __get_hh_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_total"
    
    ## 8
    @staticmethod
    def __get_indv_sen_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_sen_hh_wminor"
    
    ## 9
    @staticmethod
    def __get_indv_sen_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_sen_hh_wominor"
    
    ## 10
    @staticmethod
    def __get_indv_sen_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_sen_total"
    
    ## 11
    @staticmethod
    def __get_indv_adult_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_adult_hh_wminor"
    
    ## 12
    @staticmethod
    def __get_indv_adult_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_adult_hh_wominor"
    
    ## 13
    @staticmethod
    def __get_indv_adult_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_adult_total"
    
    ## 14
    @staticmethod
    def __get_indv_child_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_child_hh_wminor"
    
    ## 15
    @staticmethod
    def __get_indv_child_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_child_hh_wominor"
    
    ## 16
    @staticmethod
    def __get_indv_child_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_child_total"
    
    ## 17
    @staticmethod
    def __get_indv_total_hh_wminor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_total_hh_wminor"
    
    ## 18
    @staticmethod
    def __get_indv_total_hh_wominor(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_total_hh_wominor"
    
    ## 19
    @staticmethod
    def __get_indv_total(params, services:DataFrame, service_types:DataFrame):
        return "__get_indv_total"
    
    ## 20
    @staticmethod
    def __get_hh_wsenior(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_wsenior"
    
    ## 21
    @staticmethod
    def __get_hh_wosenior(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_wosenior"
    
    ## 22
    @staticmethod
    def __get_hh_grandparent(params, services:DataFrame, service_types:DataFrame):
        return "__get_hh_grandparent"

    ## error, none
    @staticmethod
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
