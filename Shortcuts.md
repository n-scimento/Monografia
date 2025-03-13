# Python

```Python
import os

os.system("pip install library")  # Ensure pip is installed
```

## Pandas: loc x iloc
- loc: by row or column name
- iloc: by row or column index

Examples: 

```Python
import pandas as pd

df = pd.DataFrame({'A': [10, 20, 30], 'B': [40, 50, 60]}, index=['a', 'b', 'c'])

# Using .loc with labels
print(df.loc['a'])     # Select row with index 'a'
print(df.loc['a':'b']) # Select rows 'a' to 'b' (both inclusive)
print(df.loc[:, 'A'])  # Select all rows for column 'A'

print(df.iloc[0])       # Select the first row
print(df.iloc[0:2])     # Select first two rows (index 0 and 1)
print(df.iloc[:, 1])    # Select all rows for the second column
```

# Docker

## New libraries
docker compose up --build --remove-orphans
(click at "Remote Python...")

# Git

## Updating project

1. git add .

2. git commit -m "name"

3. git push origin main

## Creating new branch

1. git checkout -b "name"

2. git commit -m "name"

3. git push origin {branch}

---
### Checking out from branch and merging 

1. git checkout {branch-to-go-back}

2. git merge {branch-name}

3. git push origin main 

## From other device

1. git clone https://github.com/n-scimento/Monografia.git

### To update

1. git pull 
