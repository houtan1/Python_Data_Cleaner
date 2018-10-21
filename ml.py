import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as st
import statsmodels as sm
import warnings
from time import strptime

path = "data/larvae.tab"
df = pd.read_table(path, index_col=False)

# Lowercase column names for ease of use
df.columns = df.columns.str.lower()

def filter_duplicate_columns(df):
	# Remove columns with the exact same values by transposing the data, then re-transposing
	df = df.T.drop_duplicates().T

	# Column types are lost so we force a recheck
	df = df.infer_objects()

	return df

def filter_duplicate_rows(df):
	# Remove rows with the exact same values
	df = df.drop_duplicates()

	return df

def filter_missing_values(df):
	# Remove all rows that contain missing values
	df = df.dropna()

	return df

def filter_inconsistent_field_formats(df):
	# Convert separate year, month, day fields to a single DateTime column
	if 'year' in df.columns and 'month' in df.columns:
		# Add a day column if missing
		if 'day' not in df.columns:
			df["day"] = 1

		# If month is of type object (string), convert to integer
		if df["month"].dtype == np.object:
			df["month"] = df["month"].apply(lambda x: strptime(str(x),'%B').tm_mon)

		# Use Pandas to convert multiple DateTime columns to a single date column
		df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=df["day"]), errors='ignore')

		# Drop unneeded columns
		df = df.drop(columns=["year", "month", "day"])

	# TODO: Numbers

	# TODO: Boolean

	return df

def filter_outliers(df):
	# Temporarily drop all non-numeric columns
	dfnum = df.select_dtypes([np.number])

	# Create a table where each entry is marked as true or false based on whether the value falls within 3 standard
	# deviations of every other value in that column
	dfnum_bool = np.abs(dfnum - dfnum.mean()) <= (3 * dfnum.std())

	# Filter out all rows that have at least one value outside the standard deviation
	df = df[(dfnum_bool).all(axis=1)]

	return df

# FILTER STAGE 1: REMOVE DUPLICATE COLUMNS
df = filter_duplicate_columns(df)

# FILTER STAGE 2: REMOVE DUPLICATE ROWS
df = filter_duplicate_rows(df)

# FILTER STAGE 3: MISSING VALUES
df = filter_missing_values(df)

# FILTER STAGE 4: FIELD FORMAT INCONSISTENCIES
df = filter_inconsistent_field_formats(df)

# FILTER STAGE 5: ILLOGICAL VALUES OR OUTLIERS
#df = filter_outliers(df)

print(df.head(10))

# DISTRIBUTION FITTING
def best_fit_distribution(data, bins='fd'):
	DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

	# Get histogram of original data
	y, x = np.histogram(data, bins=bins, density=True)
	x = (x + np.roll(x, -1))[:-1] / 2.0

	# Best holders
	best_distribution = st.norm
	best_params = (0.0, 1.0)
	best_sse = np.inf # SSE = sum of squared errrors of prediction

	for distribution in DISTRIBUTIONS:
		try:
			with warnings.catch_warnings():
				warnings.filterwarnings('ignore')
				params = distribution.fit(data)

				# Separate parts of parameters
				arg = params[:-2]
				loc = params[-2]
				scale = params[-1]

				# Calculate fitted PDF and error with fit in distribution
				pdf = distribution.pdf(x, loc=loc, scale=scale, *arg) # PDF = Probability density function
				sse = np.sum(np.power(y - pdf, 2.0))

				try:
					if ax:
						pd.Series(pdf, x).plot(ax=ax)
					end
				except Exception:
					pass

				# Identify if this distribution is better
				if best_sse > sse > 0:
					best_distribution = distribution
					best_params = params
					best_sse = sse

		except Exception:
			pass

	return (best_distribution.name, best_params)

def make_pdf(dist, params, size=10000):
    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution (ppf = percentage point function)
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

column_name = "length (mm)"
field_data = df[column_name]
bins = 20

# Get the best fitting distribution
best_fit_name, best_fit_params = best_fit_distribution(field_data, bins)
print("The best distribution fit is: " + best_fit_name)

# Determine PDF for distribution
best_dist = getattr(st, best_fit_name)
pdf = make_pdf(best_dist, best_fit_params)

# Plot series
plt.figure()
ax = pdf.plot(lw=2, label='PDF', legend=True)
field_data.plot(kind='hist', bins=bins, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)
ax.set_title("Using best fit distribution: " + best_fit_name)
ax.set_xlabel(column_name)
ax.set_ylabel("Frequency")
plt.show()