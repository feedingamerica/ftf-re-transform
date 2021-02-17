class Data_Service_Switcher:
    ## 1
    def __get_services_total():
         return "__get_services_total"
    
    ## 2
    def __get_undup_hh_total():
        return "__get_undup_hh_total"
    
    ## 3
    def __get_undup_indv_total():
        return "__get_undup_indv_total"
    
    ## 4
    def __get_services_per_uhh_avg():
        return "__get_services_per_uhh_avg"
    
    ## 5
    def __get_hh_wminor():
        return "__get_hh_wminor"
    
    ## 6
    def __get_hh_wominor():
        return "__get_hh_wominor"
    
    ## 7
    def __get_hh_total():
        return "__get_hh_total"
    
    ## 8
    def __get_indv_sen_hh_wminor():
        return "__get_indv_sen_hh_wminor"
    
    ## 9
    def __get_indv_sen_hh_wominor():
        return "__get_indv_sen_hh_wominor"
    
    ## 10
    def __get_indv_sen_total():
        return "__get_indv_sen_total"
    
    ## 11
    def __get_indv_adult_hh_wminor():
        return "__get_indv_adult_hh_wminor"
    
    ## 12
    def __get_indv_adult_hh_wominor():
        return "__get_indv_adult_hh_wominor"
    
    ## 13
    def __get_indv_adult_total():
        return "__get_indv_adult_total"
    
    ## 14
    def __get_indv_child_hh_wminor():
        return "__get_indv_child_hh_wminor"
    
    ## 15
    def __get_indv_child_hh_wominor():
        return "__get_indv_child_hh_wominor"
    
    ## 16
    def __get_indv_child_total():
        return "__get_indv_child_total"
    
    ## 17
    def __get_indv_total_hh_wminor():
        return "__get_indv_total_hh_wminor"
    
    ## 18
    def __get_indv_total_hh_wominor():
        return "__get_indv_total_hh_wominor"
    
    ## 19
    def __get_indv_total():
        return "__get_indv_total"
    
    ## 20
    def __get_hh_wsenior():
        return "__get_hh_wsenior"
    
    ## 21
    def __get_hh_wosenior():
        return "__get_hh_wosenior"
    
    ## 22
    def __get_hh_grandparent():
        return "__get_hh_grandparent"

    ## error, none
    def get_data_def_error():
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
