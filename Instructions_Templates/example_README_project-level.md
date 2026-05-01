# General Information

**Project title:** Transcriptomic and physiological responses of lettuce (Lactuca sativa) to nitrogen limitation  
**Date:** 2026-05-01

## Researcher Information (WHO)

**Name:** Jane Doe  
**ORCID:** 0000-0002-1234-5678  
**Institution:** Utrecht University  
**Address:** Utrecht, The Netherlands  
**Email:** j.doe@uu.nl  

## Co-Researcher(s) Information

**Name:** John Smith  
**ORCID:** 0000-0003-9876-5432  
**Institution:** Wageningen University & Research  
**Address:** Wageningen, The Netherlands  
**Email:** john.smith@wur.nl  

[Add additional co-researchers if needed]

## Project overview (WHY)

**Purpose, goals, and scope:**  
This project investigates the molecular and physiological responses of lettuce (Lactuca sativa) to nitrogen limitation. The aim is to identify gene expression changes associated with nitrogen stress and link these to phenotypic traits such as biomass accumulation and growth performance. The project integrates transcriptomic (RNA-seq), targeted gene validation (qPCR), and phenotypic measurements.

## Data structure and access (WHAT + WHERE)

Each dataset is treated as a self-contained unit with its own README and internal structure.

### Datasets

**Dataset: RNA sequencing (RNA-seq)**

**Path:** /RNAseq/README.md  
**Type:** Transcriptomics  
**Scope:** Leaf tissue samples collected at two nitrogen treatments (control vs low nitrogen) across three biological replicates  
**Description:** Raw sequencing reads (FASTQ), aligned reads (BAM), and gene-level count matrices derived from RNA sequencing of lettuce leaf tissue.

**Dataset: qPCR validation**

**Path:** /qPCR/README.md  
**Type:** Gene expression validation  
**Scope:** Subset of genes selected from RNA-seq results, measured across the same biological conditions  
**Description:** Ct values and ΔΔCt calculations used to validate differential expression of selected genes.

**Dataset: Phenotyping (biomass and growth)**

**Path:** /phenotyping/README.md  
**Type:** Phenotyping  
**Scope:** Measurements taken at harvest for all plants included in RNA-seq experiment  
**Description:** Dry mass, fresh weight, and leaf area measurements used to link gene expression patterns to plant performance.

## Project folder structure (physical organisation)

The following structure shows how datasets and analyses are organised within the project.

```
project_root/
├── RNAseq/
├── qPCR/
├── phenotyping/
├── analysis/
├── scripts/
└── project_README.md
```

Each dataset folder contains its own dataset-level README describing internal structure and content.

## Data organisation

Data are organised by dataset type, with each dataset containing raw data, processed outputs, and metadata.

- Raw data: FASTQ files (RNA-seq), raw Ct values (qPCR), raw measurement sheets (phenotyping)  
- Processed data: gene count matrices, normalised expression values, ΔΔCt values, summarised biomass data  
- Metadata: sample IDs, treatment conditions, replicate information, experimental design  

## Methods (HOW)

### Overall approach

Lettuce plants were grown under controlled greenhouse conditions with two nitrogen treatments (optimal vs limiting). Leaf samples were collected for RNA extraction and sequencing. Differential gene expression analysis was performed to identify nitrogen-responsive genes. Selected genes were validated using qPCR, and plant performance was assessed through phenotypic measurements.

### Shared methods and standards

**Protocols:**  
RNA extraction, library preparation for RNA-seq, and qPCR protocols standardised across all samples.  
Documentation: /protocols/rna_extraction.md  

**Instruments and infrastructure:**  
Greenhouse with controlled climate conditions, Illumina sequencing platform, qPCR thermocycler.  
Documentation: /infrastructure/greenhouse_setup.md  

**Computational tools and pipelines:**  
RNA-seq analysis performed using a standard pipeline including read alignment (STAR), gene quantification (featureCounts), and differential expression analysis (DESeq2).  
Repository or path: https://github.com/example/lettuce_rnaseq_pipeline  
Version: v1.2.0  

**Other standardised procedures (if applicable):**  
Consistent sample naming scheme and metadata annotation applied across all datasets.

## Project outputs

### External repositories

- Dataset repository (primary data): European Nucleotide Archive (ENA): https://www.ebi.ac.uk/ena/browser/view/PRJXXXX  
- Processed data repository: Zenodo: https://doi.org/10.5281/zenodo.XXXXXXX  

### Publications

- Doe, J. et al. (2026) Transcriptomic responses of lettuce to nitrogen limitation. *Plant Journal*. https://doi.org/10.xxxx/xxxxx  

## Project information

**Limitations:**  
Limited number of biological replicates and focus on a single lettuce cultivar may restrict generalisability. RNA-seq data represent a single time point.

**Assumptions:**  
Assumes uniform growth conditions across treatments and that sampled leaf tissue is representative of whole-plant responses.

**Cross-dataset considerations:**  
Sample IDs are consistent across RNA-seq, qPCR, and phenotyping datasets, allowing direct integration. Differences in measurement scale (molecular vs phenotypic) should be considered when interpreting results.
