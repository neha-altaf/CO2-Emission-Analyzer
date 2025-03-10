#load python libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

                        #loading & exploring our data set 
#load the data set
dataset=pd.read_csv(r'C:\Users\DELL\Desktop\yearly wise change in co2 emission\Year-on-year change in CO emissions.csv')
print(dataset)

print(dataset.info())
print(dataset.head(35))
print(dataset.tail(35))


                     # understanding dataset's structure,missing values,column types & arranging required values 
#look for null values
print(dataset.isnull().sum())                    

#removing code column as it's not that much necessary in our analysis
dataset.drop('Code',axis=1,inplace=True)

#change year column datatype in datetime format int64 to datetime64[ns]
dataset['Year']=pd.to_datetime(dataset['Year'], format='%Y')


#extracting record of continents
continent_list=['Asia','Europe','Africa','North America','South America','Antarctica','Oceania']
Continents=dataset[dataset.iloc[:,0].isin(continent_list)]
print(Continents)


#extracting the record of world
world=dataset[dataset.iloc[:,0].str.contains("World",case=False,na=False)]
print(world)


#extracting record of subcontinents
subcontinent_list=['Asia (excl. China and India)','Europe (excl. EU-27)','Europe (excl. EU-28)','Central African Republic','North America (excl. USA)','South Africa','European Union (27)','European Union (28)']
Subcontinents=dataset[dataset.iloc[:,0].isin(subcontinent_list)]
print(Subcontinents)

#extracting others
list=['High-income countries','Low-income countries','Lower-middle-income countries','Upper-middle-income countries','International shipping','International aviation']
others=dataset[dataset.iloc[:,0].isin(list)]
print(others)

#extracting record of countries
countries=dataset[~dataset['Entity'].isin(Continents['Entity'])&~dataset['Entity'].isin(world['Entity'])&~dataset['Entity'].isin(Subcontinents['Entity'])&~dataset['Entity'].isin(others['Entity'])]
print(countries)

                                #Exploratory Data Analysis and Visualization

#Regional trend analysis over time
plt.figure(figsize=(12,6))
sns.lineplot(x='Year',y='growth_emissions_total',estimator='median',color='white',data=countries,errorbar=None,zorder=2)
plt.gca().set_facecolor('black')
plt.grid(axis='both',linestyle='--',linewidth=0.5,zorder=1)
plt.ylabel('Emission')
plt.title('Regional Trend Analysis Of CarbonDioxide Emission Over Time')
plt.show()
#we use median here as our data have positive,negative and zeros values

#subcontinents trend analysis over time
plt.figure(figsize=(12,6))
sns.lineplot(x='Year',y='growth_emissions_total',estimator='median',color='white',data=Subcontinents,errorbar=None,zorder=2)
plt.gca().set_facecolor('black')
plt.ylabel('Emission(Millions)')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc:"{:,}".format(int(x/1000000))))
plt.grid(axis='both',linestyle='--',linewidth=0.5,zorder=1)
plt.title('Subcontinet wise Trend Analysis Of CarbonDioxide Emission over time')
plt.show()

#global trend analysis over time
plt.figure(figsize=(12,6))
sns.lineplot(x='Year',y='growth_emissions_total',estimator='median',color='white',data=world,errorbar=None,zorder=2)
plt.grid(axis='both',linestyle='--',linewidth=0.5,zorder=1)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc:"{:,}".format(int(x/1000000))))
plt.gca().set_facecolor('black')
plt.ylabel('Emission(Millions)')
plt.title('Global Trend Analysis Of CarbonDioxide Emission over time')
plt.show()

#top 3 continents with high CO2 emission 
st=Continents.groupby('Entity')['growth_emissions_total'].apply(lambda x: (x-x.median()).abs().mean())
st1=st.sort_values(ascending=False)
top_continents=st1.head(3)
print(top_continents)
plt.figure(figsize=(10,6))
top_continents.plot(kind='bar',width=0.2,align='center',color=['#ff0000','#0000ff','#008000'],zorder=2)

#Simulating smoke using scatter points
ax = plt.gca()
for bar in ax.patches:
    x = bar.get_x() + bar.get_width() / 2  # Center of the bar
    height = bar.get_height()

    # Generate random smoke points
    num_smoke_particles = 200  # Increase for denser smoke
    x_offsets = np.random.uniform(-0.1, 0.1, num_smoke_particles)  # Random horizontal spread
    y_offsets = np.random.uniform(0, height * 0.8, num_smoke_particles)  # Random vertical rise

    # Scatter smoke particles with WHITE color for visibility
    ax.scatter(x + x_offsets, height + y_offsets, color='white', alpha=0.15, s=15)  # Light & visible smoke
plt.gca().set_facecolor('black')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc:"{:,}".format(int(x/1000000))))
plt.title('Top 3 Continents With Highest Increase In Carbon-Dioxide Emission')
plt.grid(axis='y',linestyle='--',linewidth=0.5,zorder=1)
plt.ylabel('Emission (Millions)')
plt.show()



# top 5 countries with largest increase in CO2 emission

ch=countries.groupby('Entity')['growth_emissions_total'].apply(lambda x: (x-x.median()).abs().mean())
ch1=ch.sort_values(ascending=False)
top_countries=ch1.head(5)
print(top_countries)

sns.lineplot(color='white',data=top_countries,marker='o',zorder=2)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc:"{:,}".format(int(x/1000000))))
plt.grid(axis='both',linestyle='--',linewidth=0.5,zorder=1)
plt.gca().set_facecolor('black')
plt.xlabel("")
plt.ylabel("")
plt.ylabel('Carbondioxide emission (Millions)')
plt.title('Top 5 Countries With High Growth Emission')
plt.show()


#top 5 countries with largest decrease in CO2 emission
bm=countries.groupby('Entity')['growth_emissions_total'].apply(lambda x: (x-x.median()).abs().mean()).reset_index()
bm1=bm.sort_values(by='growth_emissions_total',ascending=True)
bm_countries=bm1.head(5)
print(bm_countries)

sns.lineplot(x='Entity',y='growth_emissions_total',color='white',data=bm_countries,marker='o',zorder=2)
plt.grid(axis='both',linestyle='--',linewidth=0.5,zorder=1)
plt.gca().set_facecolor('black')
plt.xlabel("")
plt.ylabel("")
plt.xticks(rotation=15)
plt.ylabel('Carbondioxide emission')
plt.title('Top 5 Countries With largest Decrease in Carbon-Dioxide Emission')
plt.show()



#yearly emission change comparison of China,US & Russia

def plot_emission(ax, data, country, color='white'):
    df = data[data['Entity'] == country]
    
    sns.lineplot(ax=ax, x='Year', y='growth_emissions_total', color=color, data=df, errorbar=None, zorder=2)
    
    ax.grid(axis='both', linestyle='--', linewidth=0.5, zorder=1)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x / 1_000_000))))
    ax.set_facecolor('#03055B')
    
    ax.set_xlabel("")
    ax.set_ylabel("Emission (Millions)")
    ax.set_title(f"{country}'s Yearly Emission of Carbon Dioxide", fontsize=12)

# Create subplots
fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)

# Plot emissions for each country
plot_emission(axes[0], countries, "China")
plot_emission(axes[1], countries, "Russia")
plot_emission(axes[2], countries, "United States")

# Adjust layout and show
plt.tight_layout()
plt.show()

