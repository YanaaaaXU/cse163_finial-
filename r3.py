import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv('Crime_Data_USA.csv')
d = pd.read_csv('ucr_by_state.csv')
country = gpd.read_file('gz_2010_us_040_00_5m.json')

def convert(x):
    output = x.split(',')
    output = "".join(output)
    return int(output)
  
def toString(x):
    return str(x)

def plot(d):
    cols = ['jurisdiction','crime_reporting_change','crimes_estimated','state_population','violent_crime_total','property_crime_total']
    df2 = d.drop(cols, axis=1)
    for i in df2.columns:
      df2[i] = df2.get(i).fillna(-1)
      df2[i] = df2.get(i).apply(toString)
      df2[i] = df2.get(i).apply(convert)
      newdf = df2.groupby('year').sum().reset_index()
      newdf.rename(columns={'murder_manslaughter': 'Murder',
                      'rape_legacy': 'Rape',
                      'agg_assault': 'Aggravated assault',
                      'vehicle_theft': 'Vehicle theft',
                      'larceny': 'Larceny Theft',
                      'robbery': 'Robbery',
                      'burglary': 'Burglary'}, inplace=True)
    fig, ax = plt.subplots(1, figsize=(10, 10))
    newdf.plot(ax = ax,
           x = "year",
           y=['Murder',
              'Rape',
              'Aggravated assault',
              'Vehicle theft',
              'Larceny Theft',
              'Robbery',
              'Burglary'],
              figsize=(10, 10),
              grid = True)
    ax.set_ylabel("Sum of crime(in million)")
    ax.set_title("The trend of all crimes throughout 2001-2017")
    fig.savefig("crime_factor_trend.png")

def plot2(data):
    data.sum(axis=0)
    cols = ['State','City','Year','Population','Violent Crime','Property Crime']
    df2 = data.drop(cols, axis=1)
    df3 = df2.sum(axis = 0)
    plt.figure(figsize=(10, 10))
    with sns.axes_style("whitegrid"):
        fig, ax = plt.subplots(1, figsize=(10, 10))
        sns.barplot((df3.values / df3.values.sum()) * 100,
                df3.index,
                orient='h', ax = ax)
        plt.title('Incidents per Crime Category')
        plt.xlabel('Incidents (%)')
        fig.savefig("crime_factor_category.png")
    
def plot3(data, country):
    filter_data = data[['State',
                    'Property Crime',
                    'Violent Crime',
                    'Population']]
    csv_data = filter_data.groupby('State').sum().reset_index()
    country = country[(country['NAME'] != 'Alaska') & (country['NAME'] != 'Hawaii')]
    csv_data['State'] = csv_data['State'].str.lower()
    country['NAME'] = country['NAME'].str.lower()
    csv_data['State'] = csv_data['State'].replace(['north carolina 5, 6, 8'],['north carolina'])
    merged_data = country.merge(csv_data,
                            left_on='NAME',
                            right_on='State',
                            how='left')
    by_county = merged_data.dissolve(by='State', aggfunc='sum')
    by_county['violent_ratio'] = by_county['Violent Crime'] / by_county['Population']
    by_county['property_ratio'] = by_county['Property Crime'] / by_county['Population']
    fig, [ax1, ax2] = plt.subplots(2, figsize=(20, 10))
    merged_data.plot(ax=ax1, vmin=0, vmax=1)
    by_county.plot(column='violent_ratio', ax=ax1, legend=True)
    merged_data.plot(ax=ax2, vmin=0, vmax=1)
    by_county.plot(column='property_ratio', ax=ax2, legend=True)
    ax1.set_title('Distribution of violent crime in 2018-2019 across US')
    ax2.set_title('Distribution of property crime in 2018-2019 across US')
    fig.savefig('violent_property_crime_Distribution.png')

def plot4(data):
    filter_data = data[['State',
                    'Property Crime',
                    'Violent Crime',
                    'Population']]
    csv_data = filter_data.groupby('State').sum().reset_index()
    plt.figure(figsize=(10, 10))
    csv_data['violent ratio'] = csv_data['Violent Crime'] / csv_data['Population']
    clrs = ['grey' if (x < max(csv_data['violent ratio'])) else 'green' for x in csv_data['violent ratio']]
    with sns.axes_style("whitegrid"):
          fig, ax = plt.subplots(1, figsize=(10, 10))
          sns.barplot(
          x = 'State',
          y = 'violent ratio',
          palette = clrs,
          data = csv_data)
          plt.xticks(rotation=-85)
          plt.title('Violent crime among all states from 2018-2019')
          fig.savefig("crime_violent.png")


def plot5(data):
    filter_data = data[['State',
                    'Property Crime',
                    'Violent Crime',
                    'Population']]
    csv_data = filter_data.groupby('State').sum().reset_index()
    plt.figure(figsize=(10, 10))
    csv_data['property ratio'] = csv_data['Property Crime'] / csv_data['Population']
    clrs = ['grey' if (x < max(csv_data['property ratio'])) else 'blue' for x in csv_data['property ratio']]
    with sns.axes_style("whitegrid"):
        fig, ax = plt.subplots(1, figsize=(10, 10))
        sns.barplot(
        x = "State",
        y = 'property ratio',
        palette = clrs,
        data = csv_data)
        plt.xticks(rotation=-85)
        plt.title('Property crime among all states from 2018-2019')
        fig.savefig("crime_property.png")

def plot6(data):
    filter_data = data[['Property Crime',
                    'Violent Crime']]
    change_variables = filter_data.melt()
    grouped_data = change_variables.groupby('variable').sum().reset_index()
    fig, ax = plt.subplots(1, figsize=(10, 10))
    plt.pie(grouped_data['value'], labels = grouped_data['variable'], shadow=True, startangle = 90,autopct='%1.1f%%',wedgeprops={'edgecolor':'black'})
    plt.title('The ratio comparison of Property Crimes and Violent Crimes')
    plt.tight_layout()
    fig.savefig("crime_pie_chart.png")

def plot7(data):
    filter_data = data[['Murder',
                    'Rape',
                    'Aggravated assault',
                    'Motor Vehicle Theft',
                    'Larceny Theft',
                    'Robbery',
                    'Burglary']]
    change_variables = filter_data.melt()
    grouped_data = change_variables.groupby('variable').sum().reset_index()
    fig, ax = plt.subplots(1, figsize=(10, 10))
    plt.pie(grouped_data['value'], labels = grouped_data['variable'],shadow=True, startangle = 90,autopct='%1.1f%%',wedgeprops={'edgecolor':'black'})
    plt.title('The ratio comparison of different crime categories ')
    plt.tight_layout()
    fig.savefig("crime_pie_factor_chart.png")

def main():
    data = pd.read_csv('Crime_Data_USA.csv')
    d = pd.read_csv('ucr_by_state.csv')
    country = gpd.read_file('gz_2010_us_040_00_5m.json')
    plot(d)
    plot1(data)
    plot2(data)
    plot3(data, country)
    plot4(data)
    plot5(data)
    plot6(data)
    plot7(data)
