import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read the populatuion data                              
population_data = pd.read_csv("world_population.csv")

# make each row of the file clear to see and use
population_data.rename(columns={
    "Country or Area": "country",
    "Year(s)": "year",
    "Value": "population"
}, inplace=True)

# Convert population data into number
population_data["population"] = pd.to_numeric(population_data["population"], errors="coerce")

# Remove rows with missing population values
population_data.dropna(subset=["population"], inplace=True)

# Filter data for years from 2000 onwards
population_data = population_data[population_data["year"] >= 2000]

# Group by country and calculate growth rate
population_growth = (
    population_data.groupby("country")
    .agg({"population": ["first", "last"]})  # Get the first and last population values
    .reset_index()
)
population_growth.columns = ["country", "population_start", "population_end"]
population_growth["growth_rate"] = (
    (population_growth["population_end"] - population_growth["population_start"])
    / population_growth["population_start"]
) * 100

# Select the top 10 countries with the highest growth rates
top_countries = population_growth.sort_values(by="growth_rate", ascending=False).head(10)

# Plot the population growth trend
plt.figure(figsize=(10, 6))
sns.barplot(
    x="growth_rate",
    y="country",
    data=top_countries,
    hue="country",
    dodge=False,
    palette="coolwarm",
    legend=False
)
plt.xlabel("Average Annual Population Growth Rate (%)") # X-is
plt.ylabel("Country")  #Y-is
plt.title("Top 10 Countries by Population Growth Rate (2000-2023)")#name the graph
plt.show()
print(population_data.describe())