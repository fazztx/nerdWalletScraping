# %% [markdown]
# # NerdWallet Web Scraping Tool
# 
# ### ETL tool to display high yield online savings account
# 

# %%
import pandas as pd
import numpy as np

import re

URL = "https://www.nerdwallet.com/best/banking/high-yield-online-savings-accounts"

# %% [markdown]
# #### Preview data below
# 

# %%
allTables = pd.read_html(URL) #All tables is a list with all the tables featured on the URL
df = pd.DataFrame(allTables[1]) 
df #To preview table

# %% [markdown]
# #### Keeping relevant columns
# 

# %%
df = df[['Financial Institution', 'APY', 'Minimum balance to open']] #To erase nerdwallet rating

# %% [markdown]
# #### Removing 'FDIC' from bank name
# 

# %%
data = df['Financial Institution']

i=0
while len(data) > i:
    s = str(data[i])

    #block below from copilot
    match = re.match(r'([^,]+),', s) 
    if match: 
        substring = match.group(1) 
        data[i] = substring
    i += 1

# %% [markdown]
# #### Renaming APY column
# 

# %%
df.rename(columns={"APY": "APY (%)"}, inplace=True)

# %% [markdown]
# #### Removing percentage from each APY row
# 

# %%
data = df['APY (%)']

i=0
while len(data) > i:
    s = str(data[i])

    #block below from copilot
    match = re.match(r'([^%]+)%', s) 
    if match: 
        substring = match.group(1) 
        data[i] = substring
    i += 1

# %% [markdown]
# #### Deleting redundancy in balance rows
# 

# %%
data = df['Minimum balance to open']

i=0
while len(data) > i:
    s = str(data[i])

    match = re.match(r'\$\d+(\.\d{2})?', s) #One liner from Copilot

    if match:
        substring = match.group(0)
        data[i] = substring

    else:
        data[i] = ""
    
    i+=1

# %% [markdown]
# #### Sorting based on highest APY %
# 

# %%
df.sort_values(by=['APY (%)'], ascending=False)
df.head(10)


