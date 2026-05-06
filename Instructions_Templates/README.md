# README.md (project-level)

_Estimated reading time: 5–8 minutes_

# Index

- What’s the matter?
- What’s the problem?
- What to do about it?
- How to do it?
- Folder structure (the baking book)
- Documentation layers
- Minimum viable documentation

# What’s the matter?

Have you ever tried baking a cake without following a proper recipe?

Sometimes it works. Often it doesn’t. And the difference is usually a few small missing details.

Now replace the cake with your research project.

Years of work can become hard to understand, reproduce, or reuse if key details are missing at the end.

That is the risk we are trying to avoid here.

# What’s the problem?

We often assume that publications explain everything.

They don’t.

There is rarely enough space to properly describe datasets, variables, processing steps, or analysis decisions.

These are exactly the things that determine whether your work can actually be reused.

Sharing data only works if the structure around it is clear.

# What to do about it?

The goal is simple:

Make your work understandable without you.

For others. And for your future self.

You should not need to be around for someone to figure out what you did.

Think of it like passing a recipe to someone in another country and expecting it to still work.

# How to do it?

We do this with a small set of structured documentation files.

A consistent structure makes everything easier to navigate, reuse, and debug later.

So we separate:

- structure first
- documentation inside that structure

# Folder structure (the baking book)

This is the standard structure used across all consortium projects.

project_root/
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