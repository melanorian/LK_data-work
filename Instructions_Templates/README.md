_Estimated reading time: 5–8 minutes_

# Index

[What’s the matter?](#whats-the-matter)  
[What’s the problem?](#whats-the-problem)  
[What to do about it?](#what-to-do-about-it)  
[How to do it?](#how-to-do-it)  
[Folder structure (the baking book)](#folder-structure-the-baking-book)  
[Documentation layers](#documentation-layers)  
[Minimum viable documentation](#minimum-viable-documentation)  

# What's the matter?

Have you ever tried baking a cake without following a proper recipe?

Sometimes it works out fine. But often, small missing details make all the difference, and the result falls apart. I once ended up with a crumbly pile that did not hold together at all. There was nothing left to do but throw it away.

Now imagine that instead of a cake, we are talking about your PhD or postdoc project. Years of work, and at the end the results cannot be properly understood, reproduced, or reused because key details are missing.

That is the risk when research data is left without clear instructions, the recipe to your work.

# What’s the problem?

We often assume that publications and manuscripts explain everything, the perfect recipe to understand and reproduce our work.

In reality, there is rarely enough space to describe datasets, variables, processing steps, or analysis decisions in detail. These are exactly the details that determine whether data can actually be reused.

This is why journals and funding bodies increasingly require data and code to be shared. But sharing only works if the underlying structure is clear.

# What to do about it?

We want to ensure that others, and your future self, can understand, reproduce, and reuse your work without needing you.

Just like you would want a friend in New Zealand to successfully bake your grandmother’s apple pie and have it turn out just right.

Often we do not know what future users will need. So the goal is simple: clearly explain what you do know, without assuming prior knowledge.

# How to do it?

A few simple documentation files make the difference between usable data and lost effort.

Just as important as the recipes themselves is how they are organised.

A well-structured cookbook, where every recipe follows the same logic, makes it easy to find what you need and understand it quickly. A messy one slows everything down.

The same applies to research data: structure first, then documentation inside that structure.

# Folder structure (the baking book)

Before describing individual files, we first define how everything is organised.

This is the shared structure for all Lettuce Know projects.

## Thesis-level structure (for reference)

ProjectX_Immunity_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
├── N_Data-package-chapterN/
└── README_project.md


Each chapter is a self-contained unit.

## Standard LK data structure

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


Raw data is what came in, processed data is what becomes usable, and results are what comes out of analysis.

# Documentation layers

Instead of thinking in “dataset-level README”, it is easier to think in three layers that match the structure above.

## Project-level README

This gives the overall picture.

It explains what the project is about, how datasets relate to each other, and where everything lives.

## Processed-data README

This is the most important technical layer for reuse.

It explains what a dataset means, how it was created from raw data, and how to interpret the variables together with the code book.

## Results README

This describes how results were generated from processed data and how outputs can be reproduced.

It is about analysis, not data definition.

# What is a README file?

A README is the recipe of a part of your work.

A simple rule applies: if a decision was made, it needs to be documented.

The more decisions involved, the more important the README becomes.

## Project-level README

Describes the project, dataset list, and overall structure.

## Processed-data README

Describes what the dataset represents, how it was generated, and how to interpret it.

It always connects to the code book.

## Results README

Describes analysis steps and how outputs were generated.

# What is a Code book?

A code book is the dictionary of your dataset.

It defines variables, units, and meanings so that data can be understood without guessing.

It always belongs to the processed-data level.

# What is a Knowledge transfer file?

A knowledge transfer file contains background information that is not visible in the data itself.

It captures decisions, assumptions, and context that would otherwise get lost.

It is optional but useful for complex projects.

# Step-by-step guide

| Layer | What it tells you | Importance |
|------|------------------|------------|
| raw data | origin | low to medium |
| processed data | meaning and structure | critical |
| results | analysis output | medium |
| manuscript | narrative | external |

# Minimum viable documentation

## Project-level README

- what the project is about  
- list of datasets  
- folder structure  

## Processed-data README

- what the dataset represents  
- how it was created  
- code book reference  
- key processing decisions  

## Results README

- what analysis was done  
- how outputs were generated  
- link to processed data  
- reproducibility information  

# General advice

Don’t let perfect be the enemy of good.

If time is limited, prioritise:

1. processed data documentation first  
2. results documentation second  
3. project overview last  

Focus on clarity over completeness, and on making your work understandable without you.