"""Testing Suite - Integration

   - Author: Airi Takashima Oye
   - Date: March 5, 2021
   - Email: airioye@g.ucla.edu
"""

import pytest
from excleaks.excleaks import is_hazardous_leak, is_haz_district,\
                                is_haz_exc, is_haz_de

def test_is_haz_exc_de_integration():
  """Test the integration of is_haz_exc and is_haz_de functions"""
  expected_output_int = 2
  output_is_haz_exc = is_haz_exc('Contractor')
  output_is_haz_de = is_haz_de('Hand Tools')
  total = output_is_haz_exc + output_is_haz_de
  assert total == expected_output_int, \
  """Should show that total is equal to 2."""