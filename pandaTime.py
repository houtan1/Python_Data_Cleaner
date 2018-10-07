# import the pandas module
import pandas as pd

# read in the stripped data into a dataframe and print it
df = pd.read_table('data/Doering-etal_2018-strip.tab')
print(df)

# show if any values in the dataframe are null
isNullDf = pd.isna(df)
print(isNullDf)

# Filter out all rows that have at least one value outside the standard deviation
# df = df[(dfnum_bool).all(axis=1)]

# print out the different types for each column
print(df.dtypes)

# parse our year column as datetime format
# print(pd.to_datetime(df))
# this is hopeless, since I can't tell it specifically which combination of
# columns to use to construct a date time column
# it's trying to be smart but that breaks down unless you have at least three
# columns that specify year, month, day or some abbreviation of them


# integrate Stephen's code into mine
# try to single out a column of data and find its distribution using pandas or scipy or numpi or matplotlib?
