_Estimated reading time: 5–8 minutes_

# Index

[Introduction](#Introduction)

[Step-by-step guide to preparing your data package](#Step-by-step-guide-to-preparing-your-data-package)

# Introduction

Have you ever tried baking a cake without following a proper recipe?

Sometimes it works out fine. But more often than not, small missing details make all the difference, and the result literally falls apart. I once ended up with a crumbly pile that did not hold together at all. There was nothing left to do but throw it away.

Now imagine that instead of a cake, we are talking about your PhD or postdoc project. Years of work, only for the final results to not be properly understood, reproduced, or reused because key details are missing.

That is the risk when research data is left without clear instructions: the recipe to your work.

## What’s the problem?

We often assume that publications and manuscripts explain everything: the perfect recipe to understand and reproduce our work. In reality, there is rarely enough space to describe datasets, variable names, or processing steps in detail. Yet exactly those details may determine whether data can actually be reused. This is why journals and funding bodies increasingly require data and code to be shared, which makes careful documentation essential.

In other words, the final cake might be there, but the recipe is incomplete. You might recognise some ingredients, but you cannot reliably recreate it.

That is exactly what we want to avoid if we want our work to remain useful and have lasting impact.

## What to do about it?

We want to ensure that others, and our future selves, can reliably understand, reproduce, and reuse our work, even without us.

Just like we would want a friend in New Zealand to successfully bake our grandmother’s apple pie and have it turn out just right.

Often, we do not know what future users will need. So the goal is simple: clearly explain what we do know, without assuming prior knowledge.

We do not just share what the final cake looks like, but also how exactly it came together.

To do so, we can follow two steps:

first, the structure — the layout of your baking book
second, the documentation — the actual recipes inside

## The folder structure - layout of the baking book

You can think of the folder structure as the layout of a baking book. It is much easier to find your favourite recipe and quickly get started if the structure is well organised and each recipe follows a consistent format. Without this structure, even a well-written recipe book becomes difficult to navigate.

In your project, this corresponds to the organisation of your folders, where you structure your data and outputs in a consistent way. Typically, the processing of your data moves from raw data input, through data processing, to results.

This structure is not just about keeping things tidy. It is what allows others (and your future self) to understand what was done, how data flows through the project, and how results were produced without having to guess or reconstruct missing steps.

Therefore, within the LettuceKnow consortium we suggest the following folder structure for your individual data package as the standard for a PhD thesis. Postdocs will typically replace the thesis chapter with their manuscripts.

```
ProjectX_Topic_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
└── N_Data-package-chapterN/
```

Building on previous data releases from the LettuceKnow consortium, the following is the standard structure for a project data package:

``` 
2_Data-package-chapter2/
├── 1_raw-data/
│   ├── dataset_A/
│   ├── dataset_B/
│   └── dataset_N/
│
├── 2_processed-data/
│   ├── dataset_A/
|   ├── dataset_B/
|   └── dataset_N/
|
├── 3_results/
│   ├── dataset_A/
│   ├── dataset_B/
│   ├── dataset_N/
│   ├── Figure_1/
│   ├── Figure_2/
│   └── Figure_N/
│
├── 4_metadata-files/
│   │── README.md
│   │── code_book.csv
│   ├── other_metadata.csv
│   └── knowledge_transfer_file.md (optional) 
│
└── 5_methods-and-protocols/
|   ├── protocols_A/
|   ├── protocols_B/
|   ├── protocols_N/
|   ├── scripts_A/
|   ├── scripts_B/
|   └── scripts_N/
```

## Documentation - the recipes in your baking book

Once the structure is in place, the next step is to make sure each part of the project can be clearly understood and reproduced.

The structure tells you where the recipes are.
The documentation tells you how the cake was made.

Think of this as the recipes inside your baking book. We can use different types of documents to make sure our research (or cake) can be reproduced. Typically:

- README
- code book
- knowledge tranfer file (optional)

### What is a README file

A README file is like the recipe for our research output.

It explains what data we used, how different datasets fit together, how they were processed, and what is needed to reproduce the workflow.

### What is a Code book

A code book is like a detailed ingredient list, including explanations and necessary details for each ingredient.

It defines every variable or column in our dataset so that others can correctly interpret the data. It explains variables and units, so the dataset can be reused without guessing and our work can be reproduced.

This is an essential layer of documentation because it allows to link between documentation and actual data files.

### What is a knowledge transfer file?

A knowledge transfer file is like the author’s personal notes or recommendations in a baking book.

It contains the “behind the scenes” knowledge, explaining, for example, what decisions were made, what is not obvious from the data, and what users should be careful about. It is an optional part of the LettuceKnow documentation, but can be very useful in complex projects with a lot of implicit knowledge.

# Step-by-step guide to preparing your data package

n the next section, we will walk step by step through preparing your data package for the final data release. Not all steps will be relevant for every project, and you may need to adapt certain parts to fit your specific data.

Still, it is recommended to stay as close as possible to the shared structure and templates. This makes it much easier to navigate and reuse datasets across the Lettuce Know consortium.

If your work has already been published, it is still useful to include the metadata files in `4_metadata-files/`. These metadata files can point to the correct locations of your data and code, for example in a public repository or archived dataset, and guide users in how to access and interpret your work.

In this way, we create a complete LettuceKnow recipe book: a shared collection of well-structured, understandable “LettuceCake recipes” that allow others to retrace how each scientific “LettuceCake” was made.

## A. Create The Folder structure - Creating the layout for the LettuceKnow baking book

1. Log into YODA with your credentials  
2. Navigate to:  
   `~/research-lettuceknow-releases/1_data-releases/data-release_V3_20260630/7_individual-data-packages/`  
3. Search for the folder matching your project  
4. Create your project folder and upload your thesis (or a placeholder if not yet available)

If your thesis or manuscript is not yet finished, create a clearly labelled placeholder such as `1_empty_Thesis.pdf` or `1_draft_Thesis.pdf`.  
If parts of your thesis already exist, name it accordingly, for example: `1_chapter1-3_Thesis.pdf`.

At this stage, your project folder should follow this structure:

```
ProjectX_Topic_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
└── N_Data-package-chapterN/
```

5. Now we go one level deeper into your data package. Let’s take `2_Data-package-chapter2/` as an example and open this folder.

6. Inside each data package, we create the following five folders:

```
2_Data-package-chapter2/
├── 1_raw-data/
├── 2_processed-data/
├── 3_results/
├── 4_metadata-files/
└── 5_methods-and-protocols/
```

Ideally, every data package follows the same internal structure which is also used across the LettuceKnow consortium data releases. This makes it much easier to navigate and reuse data across different projects. 

Of course, not every project is identical. If your data requires adjustments, that is fine. But try to stay as close as possible to the shared structure so others can easily understand your work without guessing where things are.

## B. Populate your folders with data – getting the ingredients for your cake

1. You should now be able to upload your files to YODA using your preferred method. If needed, you can consult the full guide on working with YODA here or reach out for help:

[https://www.uu.nl/en/research/yoda/guide-to-yoda]

**If you are working with consortium-wide datasets, publicly available data, or data that has already been published**, you do not need to upload everything again. Storing data literally comes with a cost, so we try to avoid unnecessary duplication.

Instead, you can simply reference the data you used and focus on documenting it properly in your README files and code book and other metadata files.

## C. Document your data package - write the recipie for your LettuceCake

Now that you have created a well-structured data packe, the recipie book and all the ingredients its time to write the recipe, it is time to add the recipies, add the documentation that allows everyone to reporduce your favoiure LettuceCake. 

We will go now over the differnt files by level of imporatance. Of coures, ideally you have everythign documented as suggested in the templates, but, I will also provide some minimal viable verson.  

We will fill in the: 

1. [README.md](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_README_LK.md)

2. [code_book.csv](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_code_book.csv)

Note: If you are wondering about the choice of format for those files or you are unfamiliar with markdown (.md) please navigate to more extensive instructions below: [Go to File formats](#file-formats)

### General advice

Don’t let perfect be the enemy of good.

If time is limited:

1. Start with a minimal version of `README.md` for each chapter / publication / project + `code_book.csv`  
2. Then improve to a more complete `README.md` over time  

The goal is simple:

Make your work understandable without you.

### 1. README.md

Think of the README files as the actual recipe for one of your LettuceCakes. This is where you explain how raw ingredients (raw data) became something usable (processed data, results).

This is the most important documentation file in your data package. If someone understands this, they can actually work with your data. That's why it is worth-while to invest some extra effort in a minimial viable version and best a  complete version. 

1.1 Download: [README.md](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_README_LK.md)

1.2. Fill in a minimum viable version

- General Information  
- Overview  
- Input data  
- Code book (see below)  
- Processing and analysis summary  
    - key processing steps: [brief bullets]  
    - key analysis steps: [brief bullets]  

- Outputs (most important results generated)  
    - figures: [location or description]  
    - tables: [location or description]  
    - models / results: [location or description]  

1.3 Follow the instructions in the template to generate a more complete version

### 2. code_book

In case of the code book we want to ensure the user can correctly interpret the variables and column names in your dataset to ensure a clear understanding of the provided data. It is the document where you explain each ingredient of your LettuceCake in detail so that it turns out just right. 

2.1 Download: [code_book.csv](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_code_book.csv)

2.2 Understanding & filling in the differnt columns in the code_book.csv

`index`: A simple numbering column used to keep the code book organised. This field is mainly for readability and reference.

`code`: The exact variable or column name used in the dataset. This should match the column name exactly as it appears in the data file. Think of this as the ingredient name in your recipe.

Example: `leaf_area`, `sample_id`, `treatment_group`

`meaning`: A human-readable explanation of what the variable describes. This explains the biological or experimental meaning of the variable in plain language.

Example:`Leaf surface area measurement`, `Unique identifier for each plant sample`, `Nitrogen treatment applied to the plant`

`represents`: Describes what a single value refers to, also called the unit of observation. This is important because the same variable can represent different things depending on the level of measurement.

Example:
`per plant`, `per leaf`, `per sample`, `mean value per treatment group`

`unit`: The measurement unit used for the variable.

Example: `cm²`, `mg`, `days`, `°C`, `%`

If no physical unit exists, you can use: `categorical`, `text`, `boolean`, `ID`,...

`ontology`: Optional field linking the variable to a standardised ontology or controlled vocabulary.This improves the connection with other datasets (interoperability) and helps datasets integrate across projects and repositories.

Examples used in LettuceKnow can be found following this link: 

https://planteome.org/node/1 

- Plant Ontology (PO; example: `PO:0025034`)
- Plant Experimental Conditions Ontology (PECO; example: `PECO:0001062`)
- Plant Trait Ontology (TO; example: `TO:0000063`)

If no ontology applies, this field can be left empty.

## File formats

We use simple, open formats to keep everything accessible for future users.

### README files and Knowledge transfer files (.md)

These are written in Markdown (.md).

Reasons:
- future proof, not tied to proprietary software
- formatting makes it easy to read and write
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

### Creating files

You can always:
- download the provided templates and edit

or

- start with a plain text file
- copy a template
- save with correct extension (.md or .csv)
