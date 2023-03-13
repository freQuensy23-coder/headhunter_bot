import seaborn as sns
import matplotlib.pyplot as plt

penguins = sns.load_dataset("penguins")
# a =

p = sns.histplot(data=penguins, x="flipper_length_mm")
p.set(title=f'Top 15 skills')
fig = p.get_figure()  # рисуем график со скиллами

fig.savefig("test1", bbox_inches="tight")
p = sns.barplot(data=penguins, x="island", y="body_mass_g")
p.set(title=f'Salsry data')

fig = p.get_figure()  # рисуем график со скиллами

fig.savefig("test2", bbox_inches="tight")
