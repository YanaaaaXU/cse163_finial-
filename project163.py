import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.image as mpimg

def income_map(postcode_income, country):
  postcode_income = postcode_income[['state', 'avg_income']]
  country['NAME'] = country['NAME'].str.upper()
  postcode_income = postcode_income.replace({
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
  })
  
  postcode_income['state'] = postcode_income['state'] .str.upper()
  mean_income =  postcode_income.groupby('state')['avg_income'].mean()
  country = country[(country['NAME'] != 'ALASKA') & (country['NAME'] != 'HAWAII')]
  
  merge_file = country.merge(mean_income, left_on='NAME', right_on='state', how='left')
  merge_file
  filtered_2 = merge_file[["NAME", "geometry", "avg_income"]]
  filtered_2
  
  crime_state_2 = filtered_2.dissolve(by='NAME', aggfunc='mean')
  crime_state_2
  
  fig, ax = plt.subplots(1, figsize=(10, 10))
  crime_state_2.plot(ax=ax, color='#EEEEEE', edgecolor='#FFFFFF')
  crime_state_2.plot(ax=ax, column='avg_income',legend=True)
  plt.title("Average Income in Each States")
  fig.savefig("income_state.png")

def crime_map(crime_data, country):
  crime_data= crime_data[crime_data['Year']== 2018]
  crime_data= crime_data.loc[:, ~crime_data.columns.isin(['City','Year', 'Population', 'Arson', 'Rape'])]
  country['NAME'] = country['NAME'].str.upper()
  country = country[(country['NAME'] != 'ALASKA') & (country['NAME'] != 'HAWAII')]
  
  merge_file = country.merge(crime_data, left_on='NAME', right_on='State', how='right')
  filtered = merge_file[["State", "geometry", "Burglary", "Aggravated assault", "Motor Vehicle Theft", "Larceny Theft"]]
  
  filtered_2 = filtered.dissolve(by='State', aggfunc='mean')
  
  
  fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(20, 10))
  
  country.plot(ax=ax1, color='#EEEEEE')
  country.plot(ax=ax2, color='#EEEEEE')
  country.plot(ax=ax3, color='#EEEEEE')
  country.plot(ax=ax4, color='#EEEEEE')
  
  
  filtered_2.plot(ax=ax1, column='Burglary',legend=True)
  filtered_2.plot(ax=ax2, column='Aggravated assault',legend=True)
  filtered_2.plot(ax=ax3, column='Motor Vehicle Theft',legend=True)
  filtered_2.plot(ax=ax4, column='Larceny Theft',legend=True)
  
  ax1.set_title('Number of Burglary by States')
  ax3.set_title('Number of Aggravated assault by States')
  ax2.set_title('Number of Motor Vehicle Theft by States')
  ax4.set_title('Number of Larceny Theft by States')
  fig.savefig("crime_by_state.png")
  

def crime_income_map(crime_18, country, postcode_income):
  crime_18['State'] = crime_18['State'].str[:2]
  crime_18['State'] = crime_18['State'].str.upper()
  
  country['NAME'] = country['NAME'].str[:2]
  country['NAME'] = country['NAME'].str.upper()
  
  
  postcode_income = postcode_income[['state', 'avg_income']]
  
  crime_18= crime_18.loc[:, ~crime_18.columns.isin(['City', 'Population', 'Arson', 'Rape'])]
  crime_18  
  
  
  merge_income = postcode_income.merge(crime_18, left_on='state', right_on='State')
  
  income_crime_18= merge_income[merge_income['Year']== 2018.0]
  
  mean_income = income_crime_18.groupby('state')[['avg_income', 'Violent Crime', 'Robbery','Property Crime',
                                                  'Larceny Theft', 'Aggravated assault','Murder','Motor Vehicle Theft','Burglary']].mean()
  
  
  violent_graph = sns.jointplot(data=mean_income, y='Violent Crime', x="avg_income", kind="reg")
  violent_graph.ax_joint.set_xlabel('Average Income')
  violent_graph.ax_joint.set_ylabel('Number of Violent Crime')
  
  robbery_graph = sns.jointplot(data=mean_income,  y='Robbery', x="avg_income", kind="reg")
  robbery_graph.ax_joint.set_xlabel('Average Income')
  robbery_graph.ax_joint.set_ylabel('Number of Robbery')
  
  property_graph = sns.jointplot(data=mean_income, y='Property Crime', x="avg_income", kind="reg")
  property_graph.ax_joint.set_xlabel('Average Income')
  property_graph.ax_joint.set_ylabel('Number of Property Crime')
  
  larceny_graph = sns.jointplot(data=mean_income,  y='Larceny Theft', x="avg_income", kind="reg")
  larceny_graph.ax_joint.set_xlabel('Average Income')
  larceny_graph.ax_joint.set_ylabel('Number of Larceny Theft')
  violent_graph.savefig('violent.png')
  robbery_graph.savefig('robbery.png')
  property_graph.savefig('property.png')
  larceny_graph.savefig('larceny.png')
  
  f, axarr = plt.subplots(2, 2, figsize=(10, 10))
  axarr[0,0].imshow(mpimg.imread('violent.png'))
  axarr[0,1].imshow(mpimg.imread('robbery.png'))
  axarr[1,0].imshow(mpimg.imread('property.png'))
  axarr[1,1].imshow(mpimg.imread('larceny.png'))
  
  # turn off x and y axis
  [ax.set_axis_off() for ax in axarr.ravel()]
  plt.tight_layout()
  plt.savefig("crime_income.png")
  plt.show()
  
  
def main():
  country = gpd.read_file("gz_2010_us_040_00_5m.json")
  crime_18 = pd.read_csv('crime_18_19.csv')
  crime_data = pd.read_csv('Crime_Data_USA.csv')
  postcode_income = pd.read_csv('postcode_income.csv')
  
  income_map(postcode_income, country)
  crime_map(crime_data, country)
  crime_income_map(crime_18, country, postcode_income)
  

  
  
  if __name__ == '__main__':
    main()
