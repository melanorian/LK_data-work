# General Information

**Project title:** [Enter project title]  
**Date:** [YYYY-MM-DD]

## Researcher Information

**Name:** [First name(s), last name(s)]  
**ORCID:** [ORCID ID]  
**Institution:** [Full institution name]  
**Address:** [City, country]  
**Email:** [Email address]

[Add additional researchers if needed]

## Project overview (WHY)

**Description:**  
[Briefly describe the overall project and what types of data it contains across all datasets]

**Purpose:**  
[Why this project exists. What scientific question(s) does it address? What is the overall aim?]

**Scope:**  
[What defines the boundaries of this project, e.g. species studied, experimental system, time frame, or biological focus]

## Data structure and access (WHAT + WHERE)

Each dataset in this project is stored as a self-contained unit with its own README.

### Datasets

**Dataset: [Dataset name]**

**Path:** [Relative path to dataset folder or processed-data README]  
**Type:** [e.g. Transcriptomics, Phenotyping, Imaging, Metabolomics]  
**Scope:** [What defines this dataset, e.g. experiment, assay, timepoint, cohort]  
**Description:** [Brief description of dataset content and purpose]

[Repeat for each dataset]

## Project folder structure

```
project_root/
├── [dataset_folder_1]/
├── [dataset_folder_2]/
├── analysis/
├── scripts/
└── project_README.md
```


Each dataset folder contains its own README describing structure and content.

## Data organisation across project

- Raw data: unprocessed experimental or instrument outputs  
- Processed data: cleaned and structured datasets used for analysis  
- Metadata: sample and experimental design information  

If your structure differs, describe your organisational logic here.

## Methods overview (high level)

Methods are described at dataset level.  
This section only summarises shared or global approaches.

**Shared protocols:** [link or description]  
**Shared tools/pipelines:** [link or description]  
**Experimental systems:** [e.g. greenhouse, sequencing platform]

## Project outputs

**Publications:** [DOI or citation]  
**Repositories:** [links]

## Project information

**Limitations:** [global limitations]  
**Assumptions:** [global assumptions]  
**Cross-dataset considerations:** [important integration notes]