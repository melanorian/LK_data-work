_Estimated reading time: 5–8 minutes_

# Index

- [Introduction](#whats-the-matter)
- [Overview](#What-to-do-about-it?)
- [Step-by-step guide to preparing your data package](#Step-by-step-guide-to-preparing-your-data-package)

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

You can think of this as the layout of a baking book. It is much easier to find your favourite recipe and quickly get started if the structure is well organised and each recipe follows a consistent format. Without this structure, even well-written recipes become difficult to navigate.

In your project, this corresponds to the structure of your folders, where you store the different steps of your work, typically progressing from raw data input, through data processing, to results.

Based on previous instructions shared within the LettuceKnow consortium, the following is the expected standard structure for a PhD thesis, post docs will typically replace thesis chapter with their manuscripts:


```
ProjectX_Topic_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
└── N_Data-package-chapterN/

```

Oriented on the previous data releases from the Lettuce Know consortium, the following is the standard structure for a project data package:

``` 
2_Data-package-chapter2/
├── 1_raw-data/
│   ├── dataset_A/
│   ├── dataset_B/
│   ├── dataset_N/
│
├── 2_processed-data/
│   ├── dataset_A/
|   ├── dataset_B/
|   ├── dataset_N/
|
├── 3_results/
│   ├── dataset_A/
│   ├── dataset_B/
│   ├── dataset_N/
│   ├── Figure_1/
│   ├── Figure_2/
│   ├── Figure_N/
│
├── 4_metadata-files/
│   │── README.md
│   │── code_book.csv
│   ├── other_metadata.csv
│   ├── knowledge_transfer_file.md (optional) 
│
├── 5_methods-and-protocols/
|   ├── protocols_A/
|   ├── protocols_B/
|   ├── protocols_N/
|   ├── scripts_A/
|   ├── scripts_B/
|   ├── scripts_N/

```

# Documentation layers - the recipes in your baking book

Once the structure is in place, the next step is to make sure each part of the project can actually be understood.

Think of this as the recipes inside your baking book.

The structure tells you where recipes are.  
The documentation tells you how the cake was made.

We can use differnt types of documents to make sure our research or cake can be reproduced, typically: 

- README
- code book
- knowledge tranfer file

## What is a README file

A README file is like the recipe for your work. It explains what the data is, what is needed, and how everything fits together. 

As a rule of thumb, your README file should explain which important decision you made, expecially those not immediatly apparent. The  more decisions were made, the more important it is to explain how a document was produced. 

## What is a Code book

A code book is like a detailed ingredient list that give details on the ingredients. It should define every variable or column in your dataset so that others can correctly interpret the data. In a research context, it explains variables, units, and structure, so the dataset can be reused without guessing.

## What is a knowledge transfer file?

A knowledge transfer file contains the “behind the scenes” knowledge. It explains e.g. what decisions were made, what is not obvious from the data, and what users should be careful about.

Optional, but very useful in complex projects with loads of implicit knowledge.

# Step-by-step guide to preparing your data package

In the next section, we will walk step by step through preparing your data package for the final data release. Not all steps might be relevant, and you may need to adapt certain parts to fit your specific data.

Still, it is recommended to stay as close as possible to the shared structure and templates. This makes it much easier to navigate and reuse datasets across the Lettuce Know consortium.

If your work has already been published, it is still useful to include the metadata files in  `4_metadata-files/`. The metadat files can point the user to the correct locations of your data and code, for example in a public repository or archived dataset and guid the user in how to make use and interpret your data.

In this way, together we create a complete LettuceKnow recipe book: a shared collection of well-structured, understandable “LettuceCake recipes” that allow others to retrace how each scientific “LettuceCake” was made, even years later.

## A. Create The Folder structure - Creating the layout for the LettuceKnow baking book

1. Log into YODA with your credentials  
2. Navigate to:  
   `~/research-lettuceknow-releases/1_data-releases/data-release_V3_20260630/7_individual-data-packages/`  
3. Search for the folder matching your project  
4. Create your project folder and upload your thesis (or a placeholder if not yet available)

If your thesis is not yet finished, create a clearly labelled placeholder such as: `1_empty_Thesis.pdf`or `1_draft_Thesis.pdf` If parts of your thesis already exist, name it accordingly: `1_chapter1-3_Thesis.pdf`

At this stage, your project folder should follow this structure:

```
ProjectX_Topic_Name/
├── 1_Thesis.pdf
├── 2_Data-package-chapter2/
├── 3_Data-package-chapter3/
├── N_Data-package-chapterN/
└── README_project.md
```

5. Now we go one level deeper into your data package. Let’s take `2_Data-package-chapter2/` as an example and open this folder.

6. Inside each data package, you create the following five folders.

```
2_Data-package-chapter2/
├── 1_raw-data/
├── 2_processed-data/
├── 3_results/
├── 4_metadata-files/
├── 5_methods-and-protocols/
```

Ideally, every data package follows the same internal structure which is also used across the LettuceKnow consortium data releases. This makes it much easier to navigate and reuse data across different projects. 

Of course, not every project is identical. If your data requires adjustments, that is fine. But try to stay as close as possible to the shared structure so others can easily understand your work without guessing where things are.

## B. Populate your folders with data – getting the ingredients for your cake

1. You should now be able to upload your files to YODA using your preferred method. If needed, you can consult the full guide on working with YODA here:

[https://www.uu.nl/en/research/yoda/guide-to-yoda]

**If you are working with consortium-wide datasets, publicly available data, or data that has already been published**, you do not need to upload everything again. Storing data literally comes with a cost, so we try to avoid unnecessary duplication.

Instead, you can simply reference the data you used and focus on documenting it properly in your README files and code book and other metadata files.

## C. Document your data package - write the recipie for your LettuceCake

Now that you have created a well-structured data packe, the recipie book and all the ingredients its time to write the recipe, it is time to add the recipies, add the documentation that allows everyone to reporduce your favoiure LettuceCake. 

We will go now over the differnt files by level of imporatance. Of coures, ideally you have everythign documented as suggested in the templates, but, I will also provide some minimal viable verson.  

We will fill in the: 

1. [README.md](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_README_LK.md)

2.  [code_book.csv](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_code_book.csv)

Note: If you are wondering about the choice of format for those files or you are unfamiliar with markdown (.md) please navigate to more extensive instructions below: [Go to File formats](#file-formats)

### General advice

Don’t let perfect be the enemy of good.

If time is limited:

1. Start with a minimal version of `README.md` for each chapter / publication / project + `code_book.csv`  
2. Then improve to a more complete `README.md` over time  

The goal is simple:

Make your work understandable without you.

### 1. README.md

1.1 Download: [README.md](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_README_LK.md)

Think of the README files as the actual recipe for one part of your LettuceCakes. This is where you explain how raw ingredients (raw data) became something usable (processed data, results).

This is the most important documentation file in your data package. If someone understands this, they can actually work with your data. That's why it is worth-while to invest some extra effort in a minimial viable version and best a  complete version. 

1.2. Minimum Viable Version

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

2.1 Download: [code_book.csv](https://github.com/melanorian/LK_data-work/blob/main/Instructions_Templates/template_code_book.csv)

!!!!!!!!!!!!!!
GIVE INSTRUCTIONS HOW TO FILL IN  + MINIMAL VERSION
########### KEEP ############

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
