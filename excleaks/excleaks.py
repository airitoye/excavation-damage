"""Functions in hw5.py

   - Author: Airi Takashima Oye
   - Date: March 5, 2021
   - Email: airioye@g.ucla.edu
"""

import inspect

import pandas as pd

def is_hazardous_leak(Leak_Code_for_Reporting):
    """Create outcome variable to identify hazardous vs. non-hazardous leaks.
    Return 1 if hazardous"""
    count = 0
    if (Leak_Code_for_Reporting == "AG Hazardous") | (
        Leak_Code_for_Reporting == "Code 1"
    ):
        count += 1
    return count

def is_haz_district(District):
    """Create binary predictor using district
    Return 1 if district is top five with most excavation damage leaks"""
    count = 0
    if (
        (District == 3)
        | (District == 50)
        | (District == 38)
        | (District == 56)
        | (District == 24)
    ):
        count += 1
    return count

def is_haz_exc(Type_of_Excavator):
    """Create binary predictor using type of excavator
    Return 1 if excavator is a contractor"""
    count = 0
    if (Type_of_Excavator == "Contractor") | (
        Type_of_Excavator == "Contractor - 3rd Party"
    ):
        count += 1
    return count

def is_haz_de(Damaging_Equipment):
    """Create binary predictor using damaging equipment
    Return 1 if damaging equipment is handtool"""
    count = 0
    if Damaging_Equipment == "Hand Tools":
        count += 1
    return count