*Estimated reading time: 5–8 minutes*

# Index

- [What’s the matter?](#whats-the-matter)  
- [What’s the problem?](#whats-the-problem)  
- [What to do about it?](#what-to-do-about-it)  
- [How to do it?](#how-to-do-it)  
- [Step-by-step guide](#step-by-step-guide)  
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

# What to do about it?

We want to ensure that others, and your future self, can understand, reproduce, and reuse your work, even without you.

Just like you would want a friend in New Zealand to successfully bake your grandmother’s apple pie and have it turn out just right.

Often we do not know what future users will need. So the goal is simple: clearly explain what you do know, without assuming prior knowledge.

# How to do it?

A few documentation files can make the difference between usable data and lost effort.

## What is a README file

A README file is like the recipe for your work. It explains what the data is, what is needed, and how everything fits together.

There are two levels:

A **project-level README** describes the whole project, how datasets relate to each other, and the overall structure.

A **dataset-level README** describes one dataset in detail, what it contains, how it was generated, and how it should be used.

## What is a Code book

A code book is like a detailed ingredient list.

It defines every variable or column in your dataset so that others can correctly interpret the data.

In a research context, it explains variables, units, and structure, so the dataset can be reused without guessing.

## What is a Knowledge transfer file

A knowledge transfer file contains the “behind the scenes” knowledge.

It explains why the project exists, what decisions were made, what is not obvious from the data, and what users should be careful about.

# Step-by-step guide

## File formats

We use simple, open formats to keep everything accessible.

### README files and Knowledge transfer files (.md)

These are written in Markdown (.md).

Reasons:
- future proof, not tied to software
- easy to read and write
- widely supported

You can create them using:
- any text editor (rename .txt to .md)
- https://dillinger.io/
- https://code.visualstudio.com/

### Code book (.csv)

The code book is a CSV file because it is:
- simple and widely compatible
- readable in Excel, R, Python
- good for structured data

Alternative formats:
- .tsv
- .txt with separators

Requirements:
- consistent structure
- clear columns
- UTF-8 encoding

### Creating files

You can always:
- start with a plain text file
- copy a template
- save with correct extension (.md or .csv)

## Templates

- [Project-level README template](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_README_project-level.md)  
- [Dataset-level README template](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_README_dataset-level.md)  
- [Code book template](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_code_book.csv)  

## Examples

- [Project-level README example](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/example_README_project-level.md)  
- [Dataset-level README example](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/example_README_dataset-level.md)  
- [Code book example](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/example_code_book.csv)  

## General advice

Don’t let perfect be the enemy of good.

Focus on:
- key datasets first
- minimum viable documentation first
- clarity over completeness
- asking: would someone else understand this data?

# Minimum viable documentation

## Project-level README

- project overview, purpose, scope  
- list of datasets with paths  
- basic folder structure  

## Dataset-level README

- what the dataset is and why it exists  
- how files are organised  
- what key files contain  
- what the data represents (variables, units, rows)  
- where metadata is stored  

## Code book

The code book should be as complete as possible for all variables.

It defines every variable so the dataset can be interpreted correctly.

You may leave ontology fields empty if they do not apply.

Key rule:
- completeness matters more than brevity here

## Code book clarification

- `meaning`: what the variable describes  
- `represents`: what one value refers to (unit of observation, e.g. per sample, per plant, per gene)  
- `unit`: how it is measured  

Example:

`leaf_area`
- meaning: leaf surface measurement  
- represents: total leaf area per plant  
- unit: cm²  
