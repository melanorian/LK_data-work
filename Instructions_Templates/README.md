# README.md (project-level)

_Estimated reading time: 5–8 minutes_

# Index

- [What’s the matter?](#whats-the-matter)
- [What’s the problem?](#whats-the-problem)
- [What to do about it?](#what-to-do-about-it)
- [How to do it?](#how-to-do-it)
- [Folder structure (the baking book)](#folder-structure-the-baking-book)
- [Documentation layers](#documentation-layers)
- [Minimum viable documentation](#minimum-viable-documentation)

# What's the matter?

Have you ever tried baking a cake without following a proper recipe?

Sometimes it works out fine. But often, small missing details make all the difference, and the result falls apart. I once ended up with a crumbly pile that did not hold together at all. There was nothing left to do but throw it away.

Now imagine that instead of a cake, we are talking about your PhD or postdoc project. Years of work, and at the end the results cannot be properly understood, reproduced, or reused because key details are missing.

That is the risk when research data is left without clear instructions, the recipe to your work.

# What’s the problem?

We often assume that publications and manuscripts explain everything, the perfect recipe to understand and reproduce our work.

In reality, there is rarely enough space to describe datasets, variable names, or processing steps in detail. Exactly those details may determine whether data can actually be reused.

This is why journals and funding bodies increasingly require data and code to be shared, which makes careful documentation essential.

In other words, the final cake might be there, but the recipe is incomplete. You might recognise some ingredients, but you cannot reliably recreate it. 

That’s exactly what we want to avoid if we want our work to stay useful and have lasting impact.

# What to do about it?

We want to ensure that others, and your future self, can understand, reproduce, and reuse your work, even without you.

Just like you would want a friend in New Zealand to successfully bake your grandmother’s apple pie and have it turn out just right.

Often we do not know what future users will need. So the goal is simple: clearly explain what you do know, without assuming prior knowledge.

Not just what the final cake looks like, but how it exactly how it came together.

To do so, we separate two steps:

- first, the structure: the layout of your baking book  
- then, the documentation: the actual recipes inside  

# Folder structure - the baking book

You can think of this as the layout of a baking book. It will be much easier to find your favourite recipe and quickly get started if the layout is well chosen and each recipe is formatted consistently. Without this structure, even well-written recipes become difficult to navigate.

In your project, this corresponds to the structure of your folders, where you store the different steps of your work, usually progressing from raw data input via data processing to results.

Based on previous instructions shared inthe Lettuce Know consortium, this is the expected standard structure for a Phd thesis: 

```
ProjectX_Topic_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
├── N_Data-package-chapterN/
└── README_project.md

```

Based on previous data releases from the LettuceKnow consortium, this is a standard structure for a project.

``` 
2_Data-package-chapter2/
├── 1_raw-data/
│   ├── dataset_A/
│   ├── dataset_B/
│
├── 2_processed-data/
│   ├── dataset_A/
│   │   ├── README_processed-data.md
│   │   ├── code_book.csv
│
├── 3_results/
│   ├── dataset_A_or_analysis/
│   │   ├── README_results-level.md
│
├── 4_metadata-files/
│   ├── sample_metadata.csv
│   ├── experimental_design.csv
│
├── 5_methods-and-protocols/
├── README.md

```

Raw data is what came in.  
Processed data is what becomes usable.  
Results are what come out.

# Documentation layers

## README.md (project-level)

Gives the overall picture:

- what the project is about
- how datasets relate
- where everything lives

## README_processed-data.md

Explains:

- what a dataset represents
- how it was created from raw data
- how to interpret variables
- how it connects to code_book.csv

This is the most important layer for reuse.

## README_results-level.md

Explains:

- how results were generated
- analysis steps
- reproducibility of outputs

This is about analysis, not data definition.

# What is a README?

A README is the recipe of a part of your work.

Rule of thumb:

If a decision was made, it should be documented.

More decisions means more importance.

# What is a code book?

A code book is the dictionary of your dataset.

It defines:

- variables
- units
- meanings

It prevents guessing.

(File: template_code_book.csv / example_code_book.csv)

# What is a knowledge transfer file?

A knowledge transfer file captures things not visible in the data:

- why decisions were made
- assumptions
- edge cases
- hidden reasoning

Optional, but very useful in complex projects.

(File: template_knowledge_transfer_file.md)

# Minimum viable documentation

If you are short on time, do this:

## README_processed-data.md

- what the dataset represents
- how it was created
- code book reference
- key processing decisions

(File: template_README_processed-data.md)

## README_results-level.md

- what analysis was done
- how outputs were generated
- link to processed data
- reproducibility info

(File: template_README_results-level.md)

## README.md

- what the project is about
- list of datasets
- folder structure

(File: template_README_project-level.md)

# General advice

Don’t let perfect be the enemy of usable.

If time is limited:

1. processed data documentation first  
2. results documentation second  
3. project overview last  

The goal is simple:

Make your work understandable without you.
