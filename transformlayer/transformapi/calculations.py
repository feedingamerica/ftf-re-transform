from .services.data_service import Data_Service as ds

BIG_NUM_NAMES = ["services_total", "undup_hh_total", "undup_indv_total", "services_per_uhh_avg"]
DEFAULT_CTRL = "dummy_is_grocery_service"
DEFAULT_CTRL_VAL = "1"

class CalculationDispatcher:
    def __init__(self, request):
        self.request = request #don't modify directly
        data_list = request["ReportInfo"]
        self.params = request
        self.data_dict = CalculationDispatcher.__group_by_data_def(data_list)
        

    @staticmethod
    def __group_by_data_def(data_list):
        """Returns dict of data defs grouped by reportDictid and sorted by dataDefid
        
        data_dict is a dictionary that groups the data definitions in data_list by reportDictId
        and sorts the data definitions in each group by their dataDefId, highest to smallest
        data_dict = { 
            1: [{"reportDictId": 1, "dataDefId": 1 },   {"reportDictId": 1, "dataDefId": 2 }, ... ],
            2:  [{"reportDictId": 2, "dataDefId": 5 },   {"reportDictId": 2, "dataDefId": 6 }, ... ],
            3:  [{"reportDictId": 3, "dataDefId": 19 },   {"reportDictId": 3, "dataDefId": 20 }, ... ],
        }
        
        """

        data_dict = {}
        for item in data_list:
            entry_list = data_dict.get(item["reportDictId"])
            if entry_list is None:
                pos = item["reportDictId"]
                data_dict[pos] = [item]
            else:
                entry_list.append(item)

        for entry_list in data_dict.values():
            entry_list.sort(key = lambda e: e["dataDefId"])
        return data_dict
        
    
    #runs calculation on each data_def in data_dict
    #and appends the result of the calculation to the data_def
    #modifies: self.request
    #returns the modified data_defs as a list
    def run_calculations(self):
        for group in self.data_dict.values():
            for data_def in group:
                func = data_calc_function_switcher[data_def["dataDefId"]]
                result = func(self.params)
                data_def["value"] = result

        return self.request["ReportInfo"]
        
#Big Numbers(Default Engine MVP)

#data def 1
def __get_services_total(params):
    """Calculate number of services. DataDef 1

    Arguments:
    params - a dictionary of values to scope the queries

    Returns: num_services
    num_services - number of unduplicated services

    """
    return len(ds.get_data_for_definition(1, params))

#data def 2
def __get_undup_hh_total(params):
    """Calculate number of unique families. DataDef 2

    Arguments:
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_familes
    num_familes - number of unique families

    """
    return len(ds.get_data_for_definition(2, params))
    
#data def 3
def __get_undup_indv_total(params):
    """Calculate number of unique individuals. DataDef 3

    Arguments:
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_indv
    num_familes - number of unique individuals

    """
    return len(ds.get_data_for_definition(3, params))

#data def 4
def __get_services_per_uhh_avg(params):
    """Calculate number of services per family DataDef 4

    Arguments:
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_services_avg
    num_services_avg - average number of services per family

    """
    services, families = ds.get_data_for_definition(4, params)
    return len(services)/len(families)

#Ohio Addin

# data def 5
def __get_hh_wminor(params):
    return len(ds.get_data_for_definition(5, params))

# data def 6
def __get_hh_wominor(params):
    return len(ds.get_data_for_definition(6, params))

# data def 7
def __get_hh_total(params):
    return len(ds.get_data_for_definition(7, params))

# data def 8
def __get_indv_sen_hh_wminor(params):
    seniors_wminors = ds.get_data_for_definition(8, params)
    return seniors_wminors['served_seniors'].sum()

# data def 9
def __get_indv_sen_hh_wominor(params):
    seniors_wominors = ds.get_data_for_definition(9, params)
    return seniors_wominors['served_seniors'].sum()

# data def 10
def __get_indv_sen_total(params):
    seniors = ds.get_data_for_definition(10, params)
    return seniors['served_seniors'].sum()

# data def 11
def __get_indv_adult_hh_wminor(params):
    adults_wminors = ds.get_data_for_definition(11, params)
    return adults_wminors['served_adults'].sum()

# data def 12
def __get_indv_adult_hh_wominor(params):
    adults_wominor = ds.get_data_for_definition(12, params)
    return adults_wominor['served_adults'].sum()

# data def 13
def __get_indv_adult_total(params):
    adults = ds.get_data_for_definition(13, params)
    return adults['served_adults'].sum()

# data def 14
def __get_indv_child_hh_wminor(params):
    children = ds.get_data_for_definition(14, params)
    return children['served_children'].sum()

# data def 15
def __get_indv_child_hh_wominor(params):
    return 0

# data def 16
def __get_indv_child_total(params):
    children = ds.get_data_for_definition(16, params)
    return children['served_children'].sum()

# data def 17
def __get_indv_total_hh_wminor(params):
    served = ds.get_data_for_definition(17, params)
    return served['served_total'].sum()

# data def 18
def __get_indv_total_hh_wominor(params):
    served = ds.get_data_for_definition(18, params)
    return served['served_total'].sum()

# data def 19
def __get_indv_total(params):
    served = ds.get_data_for_definition(19, params)
    return served['served_total'].sum()

#MOFC addin
def __get_hh_wsenior(params):
    pass
def __get_hh_wosenior(params):
    pass
def __get_hh_grandparent(params):
    pass
        

    ## Data Defintion Switcher
    # usage:
    #   func = __switcher.get(id)
    #   func()
data_calc_function_switcher = {
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

def main():
    print(ds.__date_str_to_int("6/16/1998"))


if __name__=="__main__":
    main()

