# import libraries
import matplotlib.pyplot as plt
import pandas as pd

# load dataframe
df = pd.read_csv("movies.csv")
df = df[['Year', 'Rating']]

df2 = df.groupby(['Year']).mean()

df2 = df2.reset_index()

# make the plot
x = df2['Year']
y = df2['Rating']
plt.xlim(2007, 2018)
plt.ylim(6, 10)
plt.xlabel('Years')
plt.ylabel('Average Rating')
plt.title('Average rating Imdb (2008 - 2017)')

plt.plot(x, y)
plt.show()
