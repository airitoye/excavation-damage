## Business Use Case: US Utility Company

1. Statement of Problem: Natural gas pipe leaks caused by excavation damage are occurring more frequently every year beginning in 2011 to 2018. 

2. Client: US Utility Company

3. Key Business Question: Are there any features of a leak that indicate that a certain set of pipe is more susceptible to excavation damage and is there a way to lessen the likelihood of leakage? 

4. Data source: I have acquired a dataset from my company that is saved locally as a CSV. 

5. Business impact of work: On average there are around 3000 leaks caused by excavation damage on distribution gas pipeline systems every year. Suppose that for each leak, there is a 10% that the leak will lead to a hazardous and reportable incident (a damage or incident that results in 50,000 dollars or more of damage, including death of resident). Each year, potential cost of damage would be 3000 leaks * .1 * $50,000 = $15 million annually. If we can reduce the number of leaks by 1% each year, we can reduce company expenses by at least 150,000 dollars. 

6. How business will use (predicted) model to make decision(s): The business can utilize various attributes of leak that have high predictability to implement improvements to the distribution system, such as curtailing use of certain type of material of pipe. They can also use it to implement new programs to increase protective measures against excavation damage in areas that are deemed higher risk. From any successful strategies, the company could present these findings at national and international conferences to demonstrate system proficiency and further the knowledge in industry research and development. 

7. Metrics/success criteria we can monitor: Leak numbers in 2019 decreased after 2018; 2019 could serve as test year to see if predictions from model are true.

## Methodology

When I first began conducting EDA on this dataset, it was apparent that majority of the columns were categorical variables, as seen below. 

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw3_1.png)

Because many of the predictors I wanted to use were nominal categorical variables, I decided to fit the appropriate predictors into a random forest model. For feature engineering, I first created an outcome variable that indicated if a leak was hazardous or not by using the column that indicates leak severity, "Leak Code for Reporting". I then used the .cat.codes function to convert all (excluding some high dimenional date fields) categorical variables via label encoding (https://www.datacamp.com/community/tutorials/categorical-data). Some excluded columns include Detect Date and Leak Fix Date, which were high dimensional data and would be difficult to interpret in a model without parsing. Although the column District had over 40 levels, I decided to keep them in the dataset since geographical information would be beneificial in applying the results of this model to the business use case. The results of the label encoding are illustrated below: 

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw3_2.png)

I then included all applicable variables (excluding the output and those variables excluded from label encoding) to create a random forest model. The results were highly skeptical, as both the micro and macro F1 value resulted in 0.99. This indicates a leakage in the data and a need to re-evaluate the predictors included. 

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw3_3.png)

To improve the model, I excluded the predictors identified to be some of the top important features in the first model. Although the improved model yielded a much lower macro F1 value of 0.55, the micro F1 score did not decrease by much, yielding a value of 0.89. As also seen in the top 20 important features, there is also a better balance among the predictors in significance to the predicted outcome. 

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw3_4.png)

The original business question can be answered with the bar graph above. The top three predictors that contributed to the model output most were "Type of Excavator", "EIR_NA" and "District". These are significant findings, as the model indicates that knowing the type of excavator that damaged the pipe, if an EIR, or emergency incident report, was submitted to the company upon leak detection and the district of where the leak occurred contribute most in predicting if the leak will be hazardous or not. The business can potentially utilize this to target geographical areas and constituencies who should be contacted to raise awareness of gas pipelines in the ground and promote initiatives to encourage contacting the utility company before digging, one of the primary causes of an excavation damage. 

## Profiling

To improve computational speed, I first ran a code to inspect how much storage each data type in my dataset was taking. As a result, the object columns, which also happened to be columns that were unused in the analysis, were taking up the most storage of 1MB. These three columns were removed as a part of the data munging step. 

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw4_1.png)

I also added the number of jobs that should be ran parallely during the step where the random forest models are generated from the default 1 to 4. As a result of these two steps, the run time of the generation of random forest models changed from the baseline of 45.1 seconds to 25.4 seconds. 

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw4_2.png)

## Architecture Diagram

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw5_1.png)

This model will be scoring with streaming data, as it is able to take one record of leak data at a time to assess the probability of it being a hazardous leak. Between the training and scoring, much of the architecture is shared, including the data processing and feature engineering. 

## Input and Output Specifications

I used Windows 10, Anaconda version 4.9.2 and Python version 3.7.0 while working on this assignment. Prior to running the code, please enter the input in the Python script. The input is recorded on line 21 and is a pandas dictionary containing the following:

- District_Haz: if the district that the leak occurred in is in one of the five districts chosen; 1 for true, 0 for false
- Exc_Haz: if the excavator who caused the damage was a contractor; 1 for true, 0 for false
- De_Haz: if the equipment used at time of damage was a hand tool; 1 for true, 0 for false
- EIR_NA: if a request was submitted by the excavator prior to the excavation taking place; 1 for true, 0 for false

When the code is ran, the INPUT variable will be printed in the log message immediately after "Part 3: Model Training". The OUTPUT variable is also a pandas dictionary and also be printed immediately after the input. The OUTPUT contains the following:

- Leak_Haz: if leak will become hazardous; 1 for true, 0 for false 

Here is an example of what the INPUT and OUTPUT variables will look like:

- INPUT = {"District_Haz": [1], "Exc_Haz": [1], "De_Haz": [1], "EIR_NA": [1]}
- OUTPUT = {"Leak_Haz": 1}

## Testing

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw5_3.png)

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw5_4.png)

I decided to add two unit tests to validate the functionality of the feature engineering functions of is_hazardous_leak and is_haz_district. The validation for is_hazardous_leak is especially critical, as this is being used to generate the output. I used the is_haz_exc and is_haz_de to create an integration test, where each function is designated to generate a 0 or 1 depending on the value of the person who caused the damage and what equipment was used. 

## Code Coverage

![GitHub Logo](https://github.com/airitoye/excavation-damage/blob/main/img/hw5_2.png)