from django.test import TestCase
import transformapi.calculations as calc
from ..services.data_service import Data_Service as ds
from django.db import connections
import unittest
import csv
import os 
import sys


sample_scope_1 = { "Scope": {
            "startDate":"01/01/2019",
            "endDate":"12/31/2019",
            "scope_type": "hierarchy",
            "scope_field":"fb_id",
            "scope_field_value":21,
            "control_type_field":"dummy_is_grocery_service",
            "control_type_value":1
        }
}


sample_scope_2 = { "Scope": {
            "startDate":"01/01/2019",
            "endDate":"12/31/2019",
            "scope_type": "geography",
            "scope_field":"fips_cnty",
            "scope_field_value":39049,
            "control_type_field":"dummy_is_grocery_service",
            "control_type_value":1
        }
}



def read_expected():
    expected = {}
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__,'./transform_test_results.csv'), newline = '') as csvfile:
        rownum = 0
        reader = csv.reader(csvfile, dialect = 'excel')
        for row in reader:
            if rownum != 0:
                expected[row[0]] = {
                    "mofc_value" : float(row[1]) if row[1].find(".") != -1 else int(row[1]),
                    "franklin_value" : float(row[2]) if row[2].find(".") != -1 else int(row[2])
                }
            rownum += 1
    return expected


EXPECTED_RESULTS = read_expected()


class CalculationsTestCase(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.fact_services_scope1 = ds.fact_services(sample_scope_1)
    #     #ds.__fact_services = None
    #     #cls.fact_services_scope2 = ds.fact_services(sample_scope_2)
    #     #ds.__fact_services = None


    def test_get_services_total(self):
        #how to avoid repeatedly making database requests in calculation tests?
        #might want to instantiate the data service object
        #might want to pass a connection to mock database in data_service.get_fact_service
        #make data service a singleton
        func = calc.data_calc_function_switcher[1]
        result = func(1,sample_scope_1)
        self.assertEqual(result, EXPECTED_RESULTS["services_total"]["mofc_value"])
    
    def test_get_undup_hh_total(self):
        func = calc.data_calc_function_switcher[2]
        result = func(2,sample_scope_1)
        self.assertEqual(result, EXPECTED_RESULTS["undup_hh_total"]["mofc_value"])
    
    def test_get_undup_indv_total(self):
        func = calc.data_calc_function_switcher[3]
        result = func(3,sample_scope_1)
        self.assertEqual(result, EXPECTED_RESULTS["undup_indv_total"]["mofc_value"])
    def test_get_services_per_uhh_avg(self):
        func = calc.data_calc_function_switcher[4]
        result = func(4,sample_scope_1)
        self.assertAlmostEqual(result, EXPECTED_RESULTS["services_per_uhh_avg"]["mofc_value"])
    
    #Ohio Addin
    # def test_get_hh_wminor(self):
    #     pass

    # def test_get_hh_wominor(self):
    #     pass
    # def test_get_hh_total(self):
    #     pass
    # def test_get_indv_sen_hh_wminor(self):
    #     pass
    # def test_get_indv_sen_hh_wominor(self):
    #     pass
    # def test_get_indv_sen_total(self):
    #     pass
    # def test_get_indv_adult_hh_wminor(self):
    #     pass
    # def test_get_indv_adult_hh_wominor(self):
    #     pass
    # def test_get_indv_adult_total(self):
    #     pass
    # def test_get_indv_child_hh_wminor(self):
    #     pass
    # def test_get_indv_child_hh_wominor(self):
    #     pass
    # def test_get_indv_child_total(self):
    #     pass
    # def test_get_indv_total_hh_wminor(self):
    #     pass
    # def test_get_indv_total_hh_wominor(self):
    #     pass
    # def test_get_indv_total(self):
    #     pass
    # #MOFC addin
    # def test_get_hh_wsenior(self):
    #     pass
    # def test_get_hh_wosenior(self):
    #     pass
    # def test_get_hh_grandparent(self):
    #     pass


if __name__ == '__main__':
    unittest.main()