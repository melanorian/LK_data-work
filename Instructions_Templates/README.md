*Estimated reading time: 2-3 minutes*

# What's the matter?

Have you ever tried baking a cake without following a proper recipe?

Sometimes it works out fine. But often, small missing details make all the difference, and the result literally falls apart. I once ended up with a crumbly pile that did not hold together at all. There was nothing left to do but throw it away.

Now imagine that instead of a cake, we are talking about your PhD or postdoc project. Years of hard work—and at the end, the results cannot be properly understood, reproduced, or reused because of missing detail.

That is the risk when research data is left without clear instructions: the recipe to your work.

# What’s the problem?

We often assume that publications and manuscripts explain everything—the perfect recipe to understand and reproduce our work. 

In reality, there is rarely enough space to describe datasets, variable names, or processing steps in detail. Exactly those details may be the difference between successfully reproducing or reusing your work - the difference between a perfect piece of cake or a crumbly disaster.

This is why journals and funding bodies increasingly require data and code to be shared, which encourages more careful documentation.

# What to do about it?

We want to ensure that others—and your future selves—can understand, reproduce, and reuse your work, even without you. Just as you would want a friend in New Zealand to be able to bake your grandmother’s favourite apple pie and have it turn out just as perfect.

An added challenge is that we do not always know what future users will need from our data. For this reason, it is better to clearly explain what you do know, without assuming prior knowledge.

So let’s get started.

# How to do it?

This is when a few documentation files can save your work — or your favourite cake.

## What is a README file

A README file is like the recipe for your work. It describes what you are making, which ingredients you need, and the main steps to follow.

In practice, there are two levels of README files:

A **project-level README** is like the introduction to a baking book. It explains what is being made across the whole “baking book”, how the different recipes (datasets) are related, and how everything fits together.

Your scientific project-level README provides the broader context: how datasets are organised, how they relate to each other, and what the overall project is trying to achieve.

A **dataset-level README** is like a single recipe card. It describes one specific cake: what it contains, how it was made, and how it should be used.

In a research context, the dataset-level README explains at a high level what the dataset contains, how it was created, and how it should be used.

## What is a Code book

A code book is like a detailed explanation of the ingredients in your recipe. 

It specifies exactly what each ingredient is, how it is measured, and how it should be interpreted—for example, what a “cup” means or what type of chocolate is used.

In a research context, it defines every variable or column in your dataset, including data types and units, to ensure correct interpretation of the data.

## What is a Knowledge transfer file

A knowledge transfer file is like the notes from the baker who created the recipe. 

It explains why the cake was made in the first place, perhaps for Auntie Stefie’s 80th birthday—and includes the small but important things that were never written down because they were simply known to matter. For example, taking the ingredients out of the fridge in advance.

In a research context, this includes the scientific motivation, experimental design choices, hidden assumptions, known limitations or biases, and lessons learned during data generation.

# Final note

In the following sections, you will find instructions and templates for creating your own README file, code book, and knowledge transfer file.

**If you are pressed for time, please rather fill the documents in partially or superficially than not at all.** In this case, almost anything is better than nothing. If you need to prioritise, start with a project-level README file and work your way down towards a knowledge transfer file 

(importance: project-level README > dataset-level README > code book > knowledge transfer file). 

Of course, ideally you would share all files—but we live in a messy, constrained reality.

Together with your data, these files will help ensure that your work remains understandable, reusable, and therefore valuable and impactful beyond the lifetime of your project. Alternatively, they can help preserve your grandmother’s apple pie recipe for eternity (as it should be).


# Step-by-Step Guide

## File formats

To make these files as accessible as possible, we use simple and widely compatible file formats.

## README files and Knowledge Transfer Files (.md format)

Both README files and Knowledge Transfer Files are written in **Markdown (.md)** format. If you are already familiar with this format, you can skip this section.

Why this format?

- Future-proof: does not depend on proprietary tools (e.g office suite) while still supporting structure (headings, lists, emphasis)
- Simple to write: just plain text with lightweight formatting
- Widely readable: supported across many platforms and tools

A plain text file (.txt) would also work, but **Markdown is preferred** because it allows structure (titles, sections, bullet points), which makes documents easier to navigate and reuse.

## Getting started with Markdown files

If you are not familiar with `.md` files, there are several easy ways to get started.

- Create a normal text file on your computer and simply rename the file extension from `.txt` to `.md`. You can then edit it using any basic text editor that supports plain text, for example Notepad (Windows) or TextEdit (Mac). This is simple and sufficient for most use cases.
- If you want to see the `.md` formatting rendered in a more visual way, you can use an online editor such as: https://dillinger.io/
- If you prefer a more powerful setup, you can use Visual Studio Code, which is a versatile and widely used tool for working with text, code, and Markdown files: https://code.visualstudio.com/

## Code book (.csv)

The Code book is provided as a **CSV file (.csv)**.

This format is used because it:
- is simple and widely compatible
- can be opened in almost any software (Excel, R, Python, etc.)
- is suitable for structured, tabular (meta)data
- integrates easily into FAIR workflows and databases

You can open `.csv` files using:
- Excel or LibreOffice Calc
- R or Python (pandas)
- any text editor (it is also human-readable as plain text)

If needed, you can also work in Excel and export the file as `.csv`.

Alternative but equivalent formats include:
- tab-delimited files (.tsv)
- text files (.txt) with comma or tab separation

All of these are acceptable as long as:
- the structure is consistent
- the columns remain clearly defined
- the encoding is preserved (preferably UTF-8)

## Creating files from scratch

If you do not want to start from a template:
- you can create a plain text file
- copy the template content into it
- and save it with the correct extension:
  - `.md` for README and Knowledge Transfer Files
  - `.csv` for the Code book
