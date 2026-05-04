# Knowledge Transfer File

Name: Jane Doe  
ORCID: 0000-0002-1234-5678  
Institution: Utrecht University  
Address: Utrecht, The Netherlands  
Email: j.doe@uu.nl  

Name: John Smith  
ORCID: 0000-0003-9876-5432  
Institution: Wageningen University & Research  
Address: Wageningen, The Netherlands  
Email: john.smith@wur.nl  

## 1. What this project was really about

This project was about understanding how lettuce reacts when nitrogen becomes limited, both at the molecular level (gene expression) and at the whole-plant level (growth and biomass).
In reality, the core challenge was not only finding differentially expressed genes, but making sure these molecular changes could be meaningfully connected to visible plant traits like biomass and leaf growth.

## 2. Key decisions (and why)

- We used two nitrogen conditions (control vs low nitrogen) because this gives a clear and interpretable stress contrast.  
- A single lettuce cultivar was chosen to reduce biological variability and keep the system controlled.  
- Leaf tissue was selected because it is the main site of nitrogen response and assimilation.  
- Three biological replicates were used as a balance between statistical power and greenhouse limitations.  
- RNA-seq was chosen as the discovery method, with qPCR used only for validation to keep the design manageable.

## 3. Things that are not obvious from the data

- Leaf samples were not always taken from exactly the same position on the plant, which may add subtle variability.  
- Plants did not respond uniformly to nitrogen stress, even within the same treatment group.  
- Small environmental differences in the greenhouse (light, humidity gradients) likely introduced minor hidden variation.  

## 4. What worked well

- The RNA extraction and sequencing workflow was stable and produced high-quality data overall.  
- STAR alignment and featureCounts quantification gave consistent results across samples.  
- The combination of RNA-seq, qPCR, and phenotyping made biological interpretation much more robust.

## 5. What did NOT work (or was changed along the way)

- An additional nitrogen timepoint was initially planned but removed due to resource constraints.  
- Some early RNA extractions showed inconsistent yield and were repeated.  
- A more complex statistical model including batch effects was tested but did not improve interpretation, so a simpler model was used.

## 6. Known issues / caveats

- Only one lettuce cultivar was studied, so results are not directly generalisable.  
- Data reflect a single developmental stage rather than a time series.  
- Moderate sample size (n=3 per condition) limits detection of subtle effects.  
- Minor batch effects between sequencing runs may still be present.

## 7. Practical tips for reuse

- Always match sample IDs across RNA-seq, qPCR, and phenotyping carefully; they are consistent but easy to misread.  
- Use normalised counts for comparisons across samples; raw counts should only be used with proper statistical models.  
- Be cautious when integrating molecular and phenotypic data due to different scales and variability.  
- If re-running analysis, keep filtering thresholds consistent with the original pipeline for comparability.

## 8. Related information

- Protocols: /protocols/rna_extraction.md  
- Codebook: /metadata/codebook_rnaseq.csv  
- Dataset README: /RNAseq/README.md  
- Pipeline: https://github.com/example/lettuce_rnaseq_pipeline (v1.2.0)
