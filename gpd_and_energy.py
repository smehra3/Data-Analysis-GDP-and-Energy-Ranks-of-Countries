
# Energy data loded from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Converted `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "..."), this is reflected as `np.NaN` values.
# 
# Renamed the following list of countries (for use in later Parts):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Removed these,
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
#
# Next, loaded the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Called this DataFrame **GDP**.
# 
# Skipped the header, and renamed the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
#
# Finally, loaded the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Called this DataFrame **ScimEn**.
#
# Joined the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Used only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
# 
# The index of this DataFrame is the name of the country, and the columns are ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].


# ### Part 1
import pandas as pd
import numpy as np
energy = pd.ExcelFile('Energy Indicators.xls').parse(skiprows=17,skip_footer=38
                                                         ,usecols=[2,3,4,5]
                                                         ,names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
countries_to_replace = {'Australia1': 'Australia',
'Bolivia (Plurinational State of)': 'Bolivia',
'China, Hong Kong Special Administrative Region3': 'Hong Kong',
'China, Macao Special Administrative Region4': 'China, Macao Special Administrative Region',
'China2': 'China',
'Denmark5': 'Denmark',
'Falkland Islands (Malvinas)': 'Falkland Islands',
'France6': 'France',
'Greenland7': 'Greenland',
'Indonesia8': 'Indonesia',
'Iran (Islamic Republic of)': 'Iran',
'Italy9': 'Italy',
'Japan10': 'Japan',
'Kuwait11': 'Kuwait',
'Micronesia (Federated States of)': 'Micronesia',
'Netherlands12': 'Netherlands',
'Portugal13': 'Portugal',
'Republic of Korea': 'South Korea',
'Saudi Arabia14': 'Saudi Arabia',
'Serbia15': 'Serbia',
'Sint Maarten (Dutch part)': 'Sint Maarten',
'Spain16': 'Spain',
'Switzerland17': 'Switzerland',
'Ukraine18': 'Ukraine',
'United Kingdom of Great Britain and Northern Ireland19': 'United Kingdom',
'United States of America20': 'United States',
'Venezuela (Bolivarian Republic of)': 'Venezuela'}
energy.replace(to_replace={'Country':countries_to_replace}, inplace=True)
energy.replace('...',np.nan, inplace=True)
energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: x*1000000)

GDP = pd.read_csv('world_bank.csv', skiprows=[0,1,2], header=1)
GDP.replace(to_replace={'Country Name':{"Korea, Rep.": "South Korea", 
                                   "Iran, Islamic Rep.": "Iran",
                                   "Hong Kong SAR, China": "Hong Kong"}}, inplace=True)
sci = pd.ExcelFile('scimagojr-3.xlsx').parse()
def part_one():
    return pd.merge(pd.merge(sci[sci['Rank']<=15], energy, how='inner',left_on='Country',right_on='Country'),
                GDP[['Country Name','2006', '2007', '2008','2009', '2010', '2011', '2012', '2013', '2014', '2015']],
                how='inner', left_on='Country', right_on='Country Name').set_index('Country').drop('Country Name', axis=1)[:15]

part_one()

# ### 2
# Previously, I joined three datasets then reduced this to just the top 15 entries. When I joined the datasets, but before I reduced this to the top 15 items, how many countries did I lose?

def part_two():
    return int(pd.merge(sci, energy, how='outer', left_on='Country', right_on='Country')
              .merge(GDP, how='outer', left_on='Country', right_on='Country Name').count()['Country'] - part_one().index.size)


part_two()
# ## The following observations are in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `part_one()`)

# ### Part 3 
# What is the average GDP over the last 10 years for each country? (excluded missing values from this calculation.)

def part_three():
    Top15 = part_one()
    Top15['avg'] = Top15[['2006', '2007', '2008','2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1)
    return Top15['avg'].sort_values(ascending = False) 

part_three()
# ### Part 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

def part_four():
    Top15 = part_one()
    Avg_6 = part_three().index[5]
    record = Top15[Top15.index.isin([Avg_6])]
    return (record['2015']-record['2006'])[0]

part_four()
# ### Part 5
# What is the mean `Energy Supply per Capita`?

def part_five():
    Top15 = part_one()
    return Top15['Energy Supply per Capita'].mean()

part_five()
# ### Part 6
# What country has the maximum % Renewable and what is the percentage?

def part_six():
    Top15 = part_one()
    df=Top15[Top15['% Renewable']==Top15['% Renewable'].max()]
    return (df.index[0], df.iloc[0]['% Renewable'])

part_six()
# ### Part 7
# What is the maximum value for this new column, and what country has the highest ratio?

def part_seven():
    Top15 = part_one()
    Top15['ratio_self_total']=[(Top15['Self-citations'][n])/Top15['Citations'][n] 
                                                  for n in Top15.index]
    Top15 = Top15.sort_values(by='ratio_self_total', ascending=False)
    return (Top15.index[0], Top15.iloc[0]['ratio_self_total'])

part_seven()
# ### Part 8
# What is the third most populous country according to Energy Supply per capita?

def part_eight():
    Top15 = part_one()
    Top15['pop_estimate']=[(Top15['Energy Supply'][n])/Top15['Energy Supply per Capita'][n] 
                                                  for n in Top15.index]
    Top15 = Top15.sort_values(by='pop_estimate', ascending=False)
    return Top15.index[2]

part_eight()
# ### Part 9 (6.6%)
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Used Pearson's correlation.

def part_nine():
    Top15 = part_one()
    Top15['pop_estimate']=[(Top15['Energy Supply'][n])/Top15['Energy Supply per Capita'][n] 
                                                  for n in Top15.index]
    Top15['citable_docs_per_person']=[(Top15['Citable documents'][n])/Top15['pop_estimate'][n] 
                                                  for n in Top15.index]
    
    return Top15[['citable_docs_per_person','Energy Supply per Capita']].corr(method ='pearson')['citable_docs_per_person']['Energy Supply per Capita']

part_nine()

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = part_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

# ### Part 10
# Created a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

def part_ten():
    Top15 = part_one()  
    #print(Top15['% Renewable'].median())
    Top15['HighRenew']=[1 if Top15['% Renewable'][n]>=Top15['% Renewable'].median() else 0
                                                  for n in Top15.index]
    return Top15['HighRenew']

part_ten()
# ### Part 11
# Used the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
#
# ContinentDict  = {'China':'Asia',
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}

def part_eleven():
    Top15 = part_one()
    Top15['pop_estimate']=[(Top15['Energy Supply'][n])/Top15['Energy Supply per Capita'][n] 
                                                  for n in Top15.index]
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    df=pd.DataFrame.from_dict(ContinentDict, orient='index')
    df.columns=['Continent']
    #conGroup.agg({'PopEst': ['sum', 'mean', 'std']})
    size_df = df.join(Top15).groupby('Continent').agg('size').to_frame()
    other_aggs = df.join(Top15).groupby('Continent').agg({'pop_estimate': ['sum', 'mean', 'std']})
    #print(size_df)
    all_joined_df = size_df.join(other_aggs)
    all_joined_df.columns=['size', 'sum', 'mean', 'std']
    return all_joined_df

part_eleven()
# ### Part 12
# Cut % Renewable into 5 bins. Grouped Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?

def part_twelve():
    Top15 = part_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    df=pd.DataFrame.from_dict(ContinentDict, orient='index')
    df.columns=['Continent']
    df['bins']=pd.cut(Top15['% Renewable'], 5)
    size_renewable = df.join(Top15).groupby(['Continent', 'bins']).agg('size')
    return size_renewable

part_twelve()
# ### Part 13
# Converted the Population Estimate series to a string with thousands separator (using commas).

def f13(row):
    return "{:,}".format(row['PopEst'])
def part_thirteen():
    Top15 = part_one()
    Top15['PopEst'] =[(Top15['Energy Supply'][n])/Top15['Energy Supply per Capita'][n] 
                                                  for n in Top15.index]
    return Top15.apply(lambda row: f13(row), axis=1).rename('PopEst')

part_thirteen()


def plot_renewable_rank():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = part_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

plot_renewable_rank()