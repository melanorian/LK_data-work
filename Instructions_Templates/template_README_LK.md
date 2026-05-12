# README.md

# General Information

**Title:** [Dataset / analysis / chapter / manuscript title]  
**Date:** [YYYY-MM-DD]  
**Version:** [e.g. v1.0]

## Contributors

**Name:** [First name(s), last name(s)]  
**ORCID:** [ORCID ID]  
**Institution:** [Institution name]  
**Email:** [Email address]

[Add more contributors if needed]

## Overview

**Description:**  
[Briefly describe what this folder contains]

**Purpose:**  
[Why was this dataset, analysis, or output generated?]

**Scope:**  
[What defines this folder, e.g. experiment, assay, manuscript chapter, analysis, cohort]

## Input data

[Describe where the data in this folder came from.]

Typically corresponds to files stored in:

- `1_raw-data/` → original experimental or instrument outputs  
- `2_processed-data/` → cleaned or transformed datasets used for downstream analysis  

Examples:

- **raw-data:** [`path or link`]  
- **processed-data:** [`path or link`]  
- **external datasets (if applicable):** [`repository / DOI / link`]

## Data interpretation

[This section usually includes documentation stored in:]

- `4_metadata-files/` → metadata, code books, annotations, and supporting documentation  

[Reference the code book used together with this folder.]

**Code book:** [`code_book.csv` or path]

[The code book defines variables, units, abbreviations, and meanings required to correctly interpret the data.]

## Biological and experimental protocols

[This section usually corresponds to files stored in:]

- `5_methods-and-protocols/` → biological protocols, experimental procedures, scripts, and workflows  

[Describe or reference the biological protocols and experimental procedures used.]

Examples:

- **sampling procedures:** [`path or link`]  
- **growth conditions:** [`path or link`]  
- **wet-lab protocols:** [`path or link`]  
- **instrument settings:** [`path or link`]  
- **experimental treatments:** [`path or link`]  
- [...]

## Data processing

[This section mainly describes how data moved from:]

- `1_raw-data/` → `2_processed-data/`

[Describe the important steps that transformed the raw data into processed data.]

### Processing steps

- **cleaning steps:** [`path or link`]  
- **filtering criteria:** [`path or link`]  
- **transformations:** [`path or link`]  
- **normalisation steps:** [`path or link`]  
- **aggregation or summarisation:** [`path or link`]  
- [...]

### Key methodological choices

- [thresholds or cut-offs]  
- [inclusion/exclusion criteria]  
- [parameter settings]  
- [...]

## Analysis and pipeline information

[This section mainly describes how data moved from:]

- `2_processed-data/` → `3_results/`

[Describe how processed data was analysed to generate outputs and results.]

### Analysis steps

- **statistical analyses:** [`path or link`]  
- **modelling approaches:** [`path or link`]  
- **comparisons performed:** [`path or link`]  
- **visualisation approaches:** [`path or link`]  
- [...]

### Scripts and workflows

**Scripts / notebooks / workflows:** [`path or link`]  
**Version:** [commit / tag / version]  
**Software/tools:** [R, Python, packages, software]  
[...]

## Results and outputs

[Describe the main outputs generated from this dataset or analysis.]

[This section usually corresponds to files stored in:]

- `3_results/` → figures, tables, models, statistical outputs, and analysis results  

Examples:

- **figures/:** [visualisations, plots, or manuscript figures]  
- **tables/:** [summary statistics, exported tables, supplementary tables]  
- **models/:** [trained models, fitted objects, or predictions]  
- **statistical_outputs/:** [tests, contrasts, enrichment analyses]  
- **other_outputs/:** [additional generated outputs]  
- [...]

## Metadata location

[Typically corresponds to files stored in:]

- `4_metadata-files/`

Examples:

- **README.md:** [`path`]  
- **code_book.csv:** [`path`]  
- **knowledge_transfer_file.md:** [`path`]  
- **sample metadata:** [`path`]  
- **experimental design:** [`path`]  
- **annotations:** [`path`]  
- [...]

## Related outputs

- [thesis chapter]  
- [manuscript]  
- [publication DOI]  
- [linked analyses]

## Notes / limitations

- [known limitations]  
- [assumptions]  
- [reuse considerations]  
- [anything important not obvious from the data]

OR/AND

If applicable:

**Knowledge transfer file:** [`knowledge_transfer_file.md` or path]
