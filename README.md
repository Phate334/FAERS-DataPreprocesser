# FAERS-DataPreprocesser
This repositore stores some script tools to clear FAERS ascii data. We use this dataset to build a website iADRs, it's can help user query the relation between drugs and adverse reactions.

# Source data issue
Not only [FAERS data files](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm082193.htm), we also process [older AERS data](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm083765.htm).

This raw data have these format issue:

* Some recodes contain newline characters(\n),it's illegal in line-oriented datafile. We check each line make sure the number of attributes is right.

# Directory Structure

    .\data
        |>2004Q1
            |>DEMO04Q1.TXT
            |>DRUG04Q1.TXT
            |> ...
        |>2004Q2
        |>2004Q3
        |> ...
