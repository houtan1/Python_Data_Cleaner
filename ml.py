import pandas
import numpy as np
import matplotlib.pyplot as plt
from time import strptime
from scipy import stats

path = "data/larvae.tab"
df = pandas.read_table(path, index_col=False)

#dataset = dataset.drop(columns=['Event', 'Longitude', 'Longitude.1', 'Station', 'Year', 'Month'])

# Lowercase column names for ease of use
df.columns = df.columns.str.lower()

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

# Convert separate year, month, day fields to a single DateTime column
if 'year' in df.columns and 'month' in df.columns:
	# Add a day column if missing
	if 'day' not in df.columns:
		df["day"] = 1

	# If month is of type object (string), convert to integer
	if df["month"].dtype == np.object:
		df["month"] = df["month"].apply(lambda x: strptime(str(x),'%B').tm_mon)

	# Use Pandas to convert multiple DateTime columns to a single date column
	df["date"] = pandas.to_datetime(dict(year=df["year"], month=df["month"], day=df["day"]), errors='ignore')

	# Drop unneeded columns
	df = df.drop(columns=["year", "month", "day"])

# TODO: Numbers

# TODO: Boolean

# FILTER STAGE 5: ILLOGICAL VALUES OR OUTLIERS

# Temporarily drop all non-numeric columns
dfnum = df.select_dtypes([np.number])

# Create a table where each entry is marked as true or false based on whether the value falls within 3 standard
# deviations of every other value in that column
dfnum_bool = np.abs(dfnum - dfnum.mean()) <= (3 * dfnum.std())

# Filter out all rows that have at least one value outside the standard deviation
df = df[(dfnum_bool).all(axis=1)]

print(df.head(10))