# General Information

**Dataset name:** RNA sequencing (RNA-seq) – lettuce nitrogen response  
**Date:** 2023-05-01  
**Version:** v1.0  

## Dataset contributors

**Name:** Jane Doe  
**ORCID:** 0000-0002-1234-5678  
**Institution:** Utrecht University  
**Email:** j.doe@uu.nl  

**Name:** John Smith  
**ORCID:** 0000-0003-9876-5432  
**Institution:** Wageningen University & Research  
**Email:** john.smith@wur.nl  

## Dataset overview

**Description:**  
This dataset contains RNA sequencing data from lettuce (Lactuca sativa) leaf tissue collected under control and nitrogen-limited conditions.

**Purpose:**  
To identify genes differentially expressed under nitrogen limitation and link transcriptional responses to physiological traits.

**Scope:**  
Leaf tissue samples from two nitrogen treatments (control vs low nitrogen), three biological replicates per treatment, single sampling time point.

## Data generation

- Plants were grown in controlled greenhouse conditions under two nitrogen regimes  
- Leaf tissue was harvested at a single developmental stage  
- RNA was extracted and sequenced using Illumina short-read sequencing  
- Raw reads were processed using a standard RNA-seq pipeline (alignment and quantification)

## File structure

```
RNAseq/
├── raw_data/
│ ├── FASTQ_files/
├── processed_data/
│ ├── gene_counts.csv
│ ├── normalized_counts.csv
├── metadata/
│ ├── sample_metadata.csv
├── scripts/
├── README.md

```

## File descriptions

- **FASTQ_files/**: Raw sequencing reads for each sample  
- **gene_counts.csv**: Raw gene-level count matrix (unfiltered)  
- **normalized_counts.csv**: Normalised expression values (DESeq2 output)  
- **sample_metadata.csv**: Sample IDs, treatment groups, and replicate information  

## Data description

- Rows represent genes (identified by gene IDs)  
- Columns represent samples  
- Values represent read counts or normalised expression levels  
- Units: raw counts (integer), normalised counts (DESeq2-normalised)

Refer to the code book for full gene annotation and variable definitions:

## Data processing

- Adapter trimming and quality filtering of raw reads  
- Alignment to lettuce reference genome using STAR  
- Gene-level quantification using featureCounts  
- Differential expression analysis using DESeq2  
- Normalisation performed within DESeq2 pipeline  

**Pipeline:** https://github.com/example/imaginary-lettuce_rnaseq_pipeline  
**Version:** v1.2.0  

## Metadata

- sample_metadata.csv includes:
  - sample IDs  
  - nitrogen treatment group  
  - replicate number  
  - sequencing batch  

## Links and references

### Related datasets

- qPCR validation dataset: /qPCR/README.md  
- Phenotyping dataset: /phenotyping/README.md  

### External repositories

- Raw data: European Nucleotide Archive (ENA) PRJXXXX  
- Processed data: Zenodo https://doi.org/10.5281/zenodo.XXXXXXX  

### Publications

- Doe, J. et al. (2026) Transcriptomic responses of lettuce to nitrogen limitation. *Plant Journal*. https://doi.org/10.xxxx/xxxxx  

## Limitations

- Single time point sampling limits temporal interpretation  
- One lettuce cultivar included  
- Moderate number of biological replicates (n=3 per treatment)

## Notes

- Sample IDs are consistent across RNA-seq, qPCR, and phenotyping datasets  
- Gene annotation may differ between reference genome versions  

