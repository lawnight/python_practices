import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

file = r"D:\code\intellij_project\warstat\logs\message.log"
keyword = 'ddff'
with open(file, 'r', encoding="utf8") as f:
    data = [x.split(' ') for x in f.readlines() if keyword in x]

df = pd.DataFrame(data)

pg, ax = plt.subplots(2, 2)
(ax1, ax2), (ax3, ax4) = ax

#df.groupby([9,12]).size().plot(kind='bar',ax=ax1)

#plt.show()


df.groupby([8,12]).size().unstack(fill_value=0).to_csv('dd.csv')
# print(df)