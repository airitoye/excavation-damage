"""Testing Suite - Unit

   - Author: Airi Takashima Oye
   - Date: March 5, 2021
   - Email: airioye@g.ucla.edu
"""

import pytest
from excleaks.excleaks import is_hazardous_leak, is_haz_district,\
                                is_haz_exc, is_haz_de

def test_is_hazardous_leak():
    """Test the is_hazardous_leak function"""
    expected_output_is_hazardous_leak = 1
    output_is_hazardous_leak = is_hazardous_leak('Code 1')
    assert output_is_hazardous_leak == expected_output_is_hazardous_leak, \
    """Should show that field has value of 1 if Leak Code is Code 1."""
   
def test_is_haz_district():
    """Test the is_hazardous_leak function"""
    expected_output_is_haz_district = 1
    output_is_haz_district = is_haz_district(50)
    assert output_is_haz_district == expected_output_is_haz_district, \
    """Should show that field has value of 1 if district is value 50."""