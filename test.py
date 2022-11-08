
#%%
import pandas as pd
import matplotlib.pyplot as plt

fn = "whole_1973-2022.csv"
df = pd.read_csv(fn)
df = df.dropna()
df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
df['year'] = df.date.apply(lambda x: x.year)

gb = dict(list(df.groupby('year')))


plt.cla()
years = [1991,2021,2022]
for year in years:
    temp = gb[year].sort_values('date').reset_index()
    lines = temp.avg.values
    plt.plot(lines,label = "%d"%year)
plt.legend()


plt.cla()
years = list(range(1973,2023))
res = []
for year in years:
    if year in gb.keys():
        temp = gb[year].sort_values('date').reset_index()
        res.append( temp.avg.mean())
plt.plot(res)

