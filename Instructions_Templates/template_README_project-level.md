# General Information

**Project title:** [Enter project title]  
**Date:** [YYYY-MM-DD]

## Researcher Information

**Name:** [First name(s), last name(s)]  
**ORCID:** [ORCID ID]  
**Institution:** [Full institution name]  
**Address:** [City, country]  
**Email:** [Email address]

## Co-Researcher(s) Information

**Name:** [First name(s), last name(s)]  
**ORCID:** [ORCID ID]  
**Institution:** [Full institution name]  
**Address:** [City, country]  
**Email:** [Email address]

[Add additional co-researchers if needed]

## Project overview (WHY)

**Purpose, goals, and scope:**  
[Describe the scientific aim and scope of the project]

## Data structure and access (WHAT + WHERE)

[e.g. each dataset is treated as a self-contained unit with its own README and internal structure.]

### Datasets

**Dataset: [Dataset name]**

**Path:** [Relative path to dataset folder or dataset-level README]  
**Type:** [e.g. Transcriptomics, Phenotyping, Imaging, Metabolomics]  
**Scope:** [What defines this dataset, e.g. experiment, assay, timepoint, cohort]  
**Description:** [Brief description of dataset content and purpose]

[Repeat this section for each dataset]

## Project folder structure (physical organisation)

The following structure shows how datasets and analyses are organised within the project.

project_root/
├── [dataset_folder_1]/
├── [dataset_folder_2]/
├── analysis/
├── scripts/
└── project_README.md

Each dataset folder should ideally contain its own dataset-level README describing its internal structure and content.

## Data organisation

If applicable, describe how data is organised across the project.  
This helps users understand how different types of data relate to each other.

Examples include:

- Raw data: [e.g. instrument outputs, unprocessed measurements]  
- Processed data: [e.g. cleaned, normalised, or analysed data]  
- Metadata: [e.g. sample information, experimental design, annotations]  

If your project does not follow this structure, describe the organisational logic used instead (e.g. by experiment, timepoint, method, or data type).

## Methods (HOW)

### Overall approach

[General experimental or analytical strategy used across the project]

### Shared methods and standards

**Protocols:**  
[Shared experimental protocols]  
Documentation: [Link or path to protocol files]

**Instruments and infrastructure:**  
[Biological infrastructure and experimental systems, e.g. greenhouse, sequencing platform, growth chambers]  
Documentation: [Link to facility or instrument documentation]

**Computational tools and pipelines:**  
[Bioinformatics tools, programming languages, scripts, workflows, statistical pipelines]  
Repository or path: [GitHub link or /analysis/pipeline/]  
Version: [Tag, release, or commit hash if applicable]

**Other standardised procedures (if applicable):**  
[Additional shared methods not covered above]

## Project outputs (WHAT resulted from this work)

### External repositories

- Dataset repository (primary data): [Name + link]  
- Processed data repository: [Name + DOI or link]  

### Publications

- [Author] ([Year]) [Title]. [Journal]. [DOI]

## Project information

**Limitations:**  
[Technical or conceptual limitations affecting interpretation]

**Assumptions:**  
[Explicit assumptions underlying experimental design or analysis]

**Cross-dataset considerations:**  
[Important considerations for integrating or comparing datasets]