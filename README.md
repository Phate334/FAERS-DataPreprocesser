# FAERS-DataPreprocesser
This repositore stores some script tools to clear FAERS ascii data. We use this dataset to build a website iADRs, it's can help user query the relation between drugs and adverse reactions.

# Source data issue
Not only [FAERS data files](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm082193.htm), we also process [older AERS data](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm083765.htm).

This raw data have these format issue:

* Some recodes contain newline characters(\n),it's illegal in line-oriented datafile. We check each line,and make sure the number of attributes is right.

* Attributes of this dataset are change four times, we are summarized in  [this](https://docs.google.com/spreadsheets/d/1EmKrWoOgbV9tZPOFrOHlHarW_TGz1uwyFuPMZ6DKGSg/edit?usp=sharing) form. Red frame indicates those not this attribute.You can see some attributes are change name like ISR, CASE. We keep all attribute name are latest version, no matter when quarterly release it. But we not remove any attribute, even it not exist in new version.

![attributes changes](http://phate334.github.io/FAERS-DataPreprocesser/attr_change.PNG)


# Directory Structure

Under each quarterly directory has 7 files, DEMO(DEMOGRAPHIC), DRUG(DRUG), REAC(REACTION), OUTC(OUTCOME), RPSR(REPORT), THER(THERAPY), INDI(INDICATIONS).

    .\data
        |>2004Q1
            |>DEMO04Q1.TXT
            |>DRUG04Q1.TXT
            |> ...
        |>2004Q2
        |>2004Q3
        |> ...
