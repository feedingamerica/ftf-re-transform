from .data_service_switcher import Data_Service_Switcher

class Data_Service:
    def get_fact_services(scope):
        return print("my function")

    def get_data_from_definition(id):
        func = Data_Service_Switcher.data_def_function_switcher.get(id, Data_Service_Switcher.get_data_def_error)
        return func()
        