# import the pandas module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in the stripped data into a dataframe and print it
df = pd.read_table('data/Doering-etal_2018-strip.tab')
print(df)

# show if any values in the dataframe are null
#isNullDf = pd.isna(df)
#print(isNullDf)

# Goal 1. Remove any duplicated columns
# the drop_duplicates() function of pandas removes rows with duplicated values
# to make this work for columns, we'll transpose the table first so columns become rows that we can detect duplications of
# note: transposing tables is very taxing, and we have to do it twice for this operation
df = df.T.drop_duplicates().T

# Goal 2. Remove any duplicated rows
# use the regular instance of the drop_duplicates() functions
df = df.drop_duplicates()

# Goal 3. Spot/Drop rows with missing field(s)
df = df.dropna()

# Goal 4. Field format inconsistencies
# print(df.dtypes)
# print(df.info())
# print(df['Depth water [m]'] + df['Temp [°C]'] + df['Longitude'])
# note, all columns show up as "object" type which is equivalent to string
# but adding those strings behaves like adding numbers...
# Stphen: we lose all concepts of types as soon as we transpose the table,
# so we need to use df = df.infer_objects() to get the correct types again
df = df.infer_objects()
# print(df.dtypes)
# print(df.info())

# Goal 5. Illogical fields values and outliers
# first, drop all non-numeric columns
dfnum = df.select_dtypes([np.number])
# note: this does not work so well...
# print(dfnum)
# Stephen's note, when inferring the object types, the types are reinstated, meaning the select_dtypes function will work properly

# then create a table where each entry is marked as true or false based on whether the value falls within 3 standard
# deviations of every other value in that column
dfnum_bool = np.abs(dfnum - dfnum.mean()) <= (3 * dfnum.std())
# print(dfnum_bool)

# Filter out all rows that have at least one value outside the standard deviation
df = df[(dfnum_bool).all(axis=1)]
# print(df)

# print out the different types for each column
# print(df.dtypes)

# parse our year column as datetime format
# print(pd.to_datetime(df))
# this is hopeless, since I can't tell it specifically which combination of
# columns to use to construct a date time column
# it's trying to be smart but that breaks down unless you have at least three
# columns that specify year, month, day or some abbreviation of them


# integrate Stephen's code into mine
# try to single out a column of data and find its distribution using pandas or scipy or numpi or matplotlib?

# Matt's histogram code

# Function Defs
def plot_hist (data, title = ""):
    fig, ax = plt.subplots()
    ax.hist(data, bins='auto')
    # bins can be auto, fd, or a number
    ax.set_title(title)
    plt.show()


lengths = df.loc[:, "H. picarti larv l [mm]"]
diam = df.loc[:, "H. picarti otolith diam [mm]"]


#fig1, ax1 = plt.subplots()
#ax1.hist(lengths, bins='fd')
#ax1.set_title("Length (mm)")

#fig2, ax2 = plt.subplots()
#ax2.hist(diam, bins=20)
#ax2.set_title("Diameter (mm)")

#plt.show()

plot_hist(diam, "H. picarti otolith diam [mm]")
plot_hist(lengths, "H. picarti larv l [mm]")

# distribution fitting, based on diameter, length, age
# next, try to fill in the missing field values
