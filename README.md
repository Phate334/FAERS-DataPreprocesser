# FAERS-DataPreprocesser
This repositore stores some script tools to clear FAERS ascii data. We use this dataset to build a website iADRs, it's can help user query the relation between drugs and adverse reactions.

## Our changes to the original data
Not only [FAERS data files](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm082193.htm), we also process [older AERS data](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm083765.htm).

### Newline character issue
Some records contain newline characters(\n),it's illegal in line-oriented datafile. We check each line,and make sure the number of attributes is right.

### Attribute changes
Attributes of this dataset are change four times, we are summarized in  [this](https://docs.google.com/spreadsheets/d/1EmKrWoOgbV9tZPOFrOHlHarW_TGz1uwyFuPMZ6DKGSg/edit?usp=sharing) form. Red frame indicates those not this attribute.You can see some attributes are change name like ISR, CASE. We keep all attribute name are latest version, no matter when quarterly release it. But we not remove any attribute, even it not exist in new version.

![attributes changes](http://phate334.github.io/FAERS-DataPreprocesser/attr_change.PNG "attributes changes")

Others issue:
* ROUTE attribute in DRUG table is SQL key word, so replace to ROUTE_.
* REPT_DT in DEMO12Q4 issue.

You can find a database's meta data in [scripts/metadata.py](https://github.com/Phate334/FAERS-DataPreprocesser/blob/master/scripts/metadata.py)

### Abnormal delimiter
In older AERS data(04Q1~12Q3), every records except INDI table are end by delimiter($). This causes inconvenience when we parse datafile. So we delete it,consistent with the new data.

![Abnormal delimiter](http://phate334.github.io/FAERS-DataPreprocesser/delimiter.png "Abnormal delimiter example")

### Append custom attributes
We append few attributes in DEMO and DRUG tables.

1. DEMO

    WT_KG: This weight attribute is calculated from WT and WT_COD, it is unified of KG.
    
    AGE_TYPE: Discretize AGE and AGE_COD attribute into 10 tags. You can check detail in [this](https://docs.google.com/document/d/1P_ZOdklUnZxJ8Hq15rtDOp_I-fls5w6Z1NZlOzlzje0/edit?usp=sharing) table.

2. DRUG

    RXCUI: We transform the DRUGNAME attrbute into rxcui code.
    
## Directory Structure

Under each quarterly directory has 7 files, DEMO(DEMOGRAPHIC), DRUG(DRUG), REAC(REACTION), OUTC(OUTCOME), RPSR(REPORT), THER(THERAPY), INDI(INDICATIONS).

    .\data
        |>2004Q1
            |>DEMO04Q1.TXT
            |>DRUG04Q1.TXT
            |> ...
        |>2004Q2
        |>2004Q3
        |> ...
