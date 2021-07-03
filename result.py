"""Final Project for STATS 404 Winter 2021

   - Author: Airi Takashima Oye
   - Date: March 16, 2021
   - Email: airioye@g.ucla.edu
"""
import logging

import joblib
import pandas as pd
import s3fs

# Create logging
# https://www.loggly.com/blog/4-reasons-a-python-logging-library-is-much-better-than-putting-print-statements-everywhere/
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Create variables
INPUT = {"District_Haz": [0], "Exc_Haz": [1], "De_Haz": [1], "EIR_NA": [1]}
s3_fs = s3fs.S3FileSystem(anon=False)

if __name__ == "__main__":
    ### ---------------------------------------------------------------------------
    ### --- Part 1: Load CSV and model from S3 Bucket
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 1: Load CSV and model from S3 Bucket")

    # Load model from S3
    ml = "s3://airitoye-stats404-project/LR_hazleaks.joblib"
    with s3_fs.open(ml, "rb") as file:
        mdl = joblib.load(file)

    # Load data from S3
    data = "https://airitoye-stats404-project.s3-us-west-1.amazonaws.com/ED-2_HW4.csv"
    df = pd.read_csv(filepath_or_buffer=data, encoding="latin-1")

    ### ---------------------------------------------------------------------------
    ### --- Part 2: Feature Engineering
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 2: Feature Engineering")

    # Rename columns for usability
    df.columns = [c.replace(" ", "_") for c in df.columns]

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

    ### ---------------------------------------------------------------------------
    ### --- Part 3: Make Prediction with User Input
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 3: Make Prediction with User Input")
    LOGGER.info("--- Input : %s", INPUT)
    INPUT = pd.DataFrame(data=INPUT)

    OUTPUT = mdl.predict(INPUT)
    OUTPUT = OUTPUT[0].astype(int)
    OUTPUT = {"Leak_Haz": OUTPUT}

    LOGGER.info("--- Output: %s", OUTPUT)
    LOGGER.info("--- Part 4: End")
