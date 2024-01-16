# Coco Member Processor

This is a program to clean the member data from Core Course.

## Data Source:

1. **Coco Member Data:**
    - Extracted from coco offline & online, with filter: member end date from 12 month prior today to NONE.
    - Include all columns except "Activities".
    - There are two files for each month. 
    - Download each file multiple times to make sure that every member data is exported.

## How to Use:

1. This file works per month. Specify month on the top of the config.py.
2. Clean the member data with main.ipynb.
3. Save cleaned member data into separate folder.

## Usage:

The output of this program is used for:

1. Raw data for Experience Management Report - Member Cohort
2. Member Population per Center Report (in Experience Management Report).
