# Data Processing: EDA week 2 - Bernar van Tongeren - 12374377

'''personal choices:

    1. I chose to delete rows with missing data,
    since taking means or medians would draw a wrong picture and
    give less information about the distribution of the data.
    I chose for less quantity to keep quality of data.
    There is not enough time (for me) for more experienced ways of imputing the missing data.

    2. I chose to show the histogram without outlier(s) normally I would also
    show the outliers so people can make their own assumptions but I checked
     on the internet and this number can't be right'''

# import libraries:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load in Dataframe with Pandas:

file = "input.csv"
df = pd.read_csv(file)
df = df[['Country', 'Region', 'Pop. Density (per sq. mi.)',
 'Infant mortality (per 1000 births)', 'GDP ($ per capita) dollars']]

# cleaning and preprocessing data:

df = df.replace('unknown', np.nan)
df = df.dropna()

# replace comma's by points to convert population density values to float:

f = lambda x: x.replace(',', '.')
df['Pop. Density (per sq. mi.)'] = df['Pop. Density (per sq. mi.)'].apply(f)
df['Infant mortality (per 1000 births)'] = df['Infant mortality (per 1000 births)'].apply(f)

# strip "dollar" of GDP and convert values to integer (two steps otherwise error):

f2 = lambda x: x.strip(' dollars')
df['GDP ($ per capita) dollars'] = df['GDP ($ per capita) dollars'].apply(f2)

f3 = lambda x: int(x)
df['GDP ($ per capita) dollars'] = df['GDP ($ per capita) dollars'].apply(f3)

# convert values of infant mortality to float:

f4 = lambda x: float(x)
df['Infant mortality (per 1000 births)'] = df['Infant mortality (per 1000 births)'].apply(f4)

# print the mean, median and the mode (GDP):

print("mean: " + str((df['GDP ($ per capita) dollars'].mean())) +
    "\nmedian: " + str(df['GDP ($ per capita) dollars'].median()) +
    "\nmode: " + str(df['GDP ($ per capita) dollars'].mode()))

# print 5 number summary:

print(df['Infant mortality (per 1000 births)'].describe())

# Delete Suriname because of (wrong) outlier:

df['GDP ($ per capita) dollars'] = df['GDP ($ per capita) dollars']\
.drop(df['GDP ($ per capita) dollars'][df['GDP ($ per capita) dollars'] > 350000].index)

# plotting Histogram of gdp:

plt.hist(df['GDP ($ per capita) dollars'],
 color = 'purple', bins = 30, histtype = 'bar')

plt.xlabel("GDP in dollars")
plt.ylabel("Frequency")
plt.title('GDP ($ per capita) in dollars across countries')
plt.show(block=False)
plt.pause(3)
plt.close()

# plotting Boxplot of the Infant mortality data:

plt.boxplot(df['Infant mortality (per 1000 births)'])
plt.ylabel('Infant mortality (per 1000 births)')
plt.title('Infant mortality Boxplot')
plt.show(block=False)
plt.pause(3)
plt.close()

# write data to JSON file:

df = df.set_index('Country')
json = df.to_json('data.json', orient = 'index')
