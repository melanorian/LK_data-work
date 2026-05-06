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
ProjectX_Immunity_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
├── N_Data-package-chapterN/
└── README_project.md
```


Each dataset folder contains its own README describing structure and content.

## Data organisation across project

```
project_root/
├── 1_raw-data/
│ ├── dataset_A/
│ ├── dataset_B/
│
├── 2_processed-data/
│ ├── dataset_A/
│ │ ├── README_processed-data.md
│ │ ├── code_book.csv
│
├── 3_results/
│ ├── dataset_A_or_analysis/
│ │ ├── README_results.md
│
├── 4_metadata-files/
│ ├── sample_metadata.csv
│ ├── experimental_design.csv
│
├── 5_methods-and-protocols/
└── README_project.md
```

- **raw-data:** original experimental or instrument outputs as they were generated. This is the starting point of the data lifecycle and should remain unchanged.

- **processed-data:** cleaned, transformed, and structured datasets that are ready for analysis. This is the first version of the data that can be meaningfully interpreted and used. It is always documented together with a code book and a dataset-level README.

- **results:** outputs generated from analysing the processed data, such as figures, tables, statistical summaries, or models. These results are typically linked to a specific analysis, chapter, or publication.

- **metadata-files:** supporting information needed to interpret the data correctly, such as sample descriptions, experimental design, and annotation tables.

- **methods-and-protocols:** shared experimental or computational procedures that apply across datasets and analyses.

If your structure differs, replace with your organisational logic.

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