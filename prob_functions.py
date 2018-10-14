# Probability functions using numpy/scipy/pandas/scikit-learn

import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Function Defs
def plot_hist (data, title = ""):
    fig, ax = plt.subplots()
    ax.hist(data, bins='fd')
    ax.set_title(title)
    plt.show()

# dataset location
path = "data/larvae.tab"

# import dataset
dset = pandas.read_table(path, index_col=False)

#list columns
#print(dset.columns)

lengths = dset.loc[:, "Length (mm)"]
diam = dset.loc[:, "Diam (mm)"]

# https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges
# bins='fd' does this
# bins='auto' takes the max of the FD distance and the Sturges method (Default in R)
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges

#fig1, ax1 = plt.subplots()
#ax1.hist(lengths, bins='fd')
#ax1.set_title("Length (mm)")
#
#fig2, ax2 = plt.subplots()
#ax2.hist(diam, bins=20)
#ax2.set_title("Diameter (mm)")

#plt.show()

plot_hist(diam)
plot_hist(lengths, "Length (mm)")
