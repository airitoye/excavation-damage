"""Final Project for STATS 404 Winter 2021

   - Author: Airi Takashima Oye
   - Date: February 23, 2021
   - Email: airioye@g.ucla.edu
"""

import inspect
import logging

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Create logging
# https://www.loggly.com/blog/4-reasons-a-python-logging-library-is-much-better-than-putting-print-statements-everywhere/
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Create variables
INPUT = {"District_Haz": [1], "Exc_Haz": [1], "De_Haz": [1], "EIR_NA": [0]}

if __name__ == "__main__":
    ### ---------------------------------------------------------------------------
    ### --- Part 1: Load data
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 1: Load data")

    # Import data with three unused columns dropped
    # Split into train and test data
    df = pd.read_csv("ED-2_HW4.csv")
    df, df_test = train_test_split(df, test_size=0.25, random_state=1)

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

    # Add to data
    df["Leak_Haz"] = df[["Leak_Code_for_Reporting"]].apply(
        lambda row: is_hazardous_leak(row[0]), axis=1
    )
    df["District_Haz"] = df[["District"]].apply(
        lambda row: is_haz_district(row[0]), axis=1
    )
    df["Exc_Haz"] = df[["Type_of_Excavator"]].apply(
        lambda row: is_haz_exc(row[0]), axis=1
    )
    df["De_Haz"] = df[["Damaging_Equipment"]].apply(
        lambda row: is_haz_de(row[0]), axis=1
    )

    # Convert categorical variables to integers to pass through model
    clmn = list(
        df.drop(columns=["Leak_Haz", "District_Haz", "Exc_Haz", "De_Haz", "EIR_NA"])
    )
    for x in clmn:
        df[x] = df[x].astype("category")
    for x in clmn:
        df[x] = df[x].cat.codes

    ### ---------------------------------------------------------------------------
    ### --- Part 3: Model Training
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 3: Model Training")

    y = df["Leak_Haz"]
    X = df[["District_Haz", "Exc_Haz", "De_Haz", "EIR_NA"]]

    inspect.signature(LogisticRegression)

    # Create a logistic regression model
    logreg_model_hazleak = LogisticRegression(
        C=0.5,
        fit_intercept=True,
        class_weight="balanced",
        random_state=1,
        max_iter=10000,
        solver="lbfgs",
    )

    # Fit logistic regression model with certain parameters to data
    logreg_model_hazleak.fit(X, y)

    # Provide model with the INPUT variable to produce output
    LOGGER.info("--- Input: %s", INPUT)
    INPUT = pd.DataFrame(data=INPUT)

    OUTPUT = logreg_model_hazleak.predict(INPUT)
    OUTPUT = OUTPUT[0].astype(int)
    OUTPUT = {"Leak_Haz": OUTPUT}

    LOGGER.info("--- Output: %s", OUTPUT)
    LOGGER.info("--- End code")