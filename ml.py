import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

path = "data/larvae.tab"
df = pandas.read_table(path, index_col=False)

#dataset = dataset.drop(columns=['Event', 'Longitude', 'Longitude.1', 'Station', 'Year', 'Month'])

# FILTER STAGE 1: REMOVE DUPLICATE COLUMNS

# Remove columns with the exact same values by transposing the data, then re-transposing
df = df.T.drop_duplicates().T

# Column types are lost so we force a recheck
df = df.infer_objects()

# FILTER STAGE 2: REMOVE DUPLICATE ROWS

# Remove rows with the exact same values
df = df.drop_duplicates()

# FILTER STAGE 3: MISSING VALUES

# Remove all rows that contain missing values
df = df.dropna()

# FILTER STAGE 4: FIELD FORMAT INCONSISTENCIES

#TODO

# FILTER STAGE 5: ILLOGICAL VALUES OR OUTLIERS

# Drop all non-numeric columns
dfnum = df.select_dtypes([np.number])

# Create a table where each entry is marked as true or false based on whether the value falls within 3 standard
# deviations of every other value in that column
dfnum_bool = np.abs(dfnum - dfnum.mean()) <= (3 * dfnum.std())

# Filter out all rows that have at least one value outside the standard deviation
df = df[(dfnum_bool).all(axis=1)]

print(df.head(10))