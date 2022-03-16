"""
Shanglin Zeng
CSE 163 group project
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def plot_15_lowest(crime_num, edu):
    """
    plot the scatter plot of the fifteen states with the lowest
    number of violent crime in the U.S
    """
    crime_num = crime_num[['State', 'Violent Crime']].dropna()
    mean_crime = crime_num.groupby('State').mean()
    top15_lowest = mean_crime.sort_values(by=['Violent Crime']).head(15)
    edu = edu[['State', "Percent of adults with a bachelor's degree or higher"]]
    mean_edu = edu.groupby('State').mean()
    crime_education_lowest = top15_lowest.merge(mean_edu, left_on='State',
                             right_on='State', how='left')
    sns.relplot(data=crime_education_lowest, x="Percent of adults with\
                a bachelor's degree or higher", y='Violent Crime',
                style='State', hue='State')
    plt.title("Fifteen States with Lowest Number of Crime")
    plt.xlabel("Percent of adults with a bachelor's degree or higher")
    plt.ylabel("Number of Violent Crime")
    plt.savefig("Lowest_fifteen_states.png")


def plot_15_lowest_reg(crime_num, edu):
    crime_num = crime_num[['State', 'Violent Crime']].dropna()
    mean_crime = crime_num.groupby('State').mean()
    top15_lowest = mean_crime.sort_values(by=['Violent Crime']).head(15)
    edu = edu[['State', "Percent of adults with a bachelor's degree or higher"]]
    mean_edu = edu.groupby('State').mean()
    crime_education_lowest = top15_lowest.merge(mean_edu, left_on='State',
                             right_on='State', how='left')
    sns.jointplot(x="Percent of adults with a bachelor's degree or higher",
                  y='Violent Crime', data=crime_education_lowest, kind="reg")
    plt.xlabel("Percent of adults with a bachelor's degree or higher")
    plt.ylabel("Number of Violent Crime")
    plt.savefig("Lowest_fifteen_states_reg.png")


def plot_15_highest(crime_num, edu):
    crime_num = crime_num[['State', 'Violent Crime']].dropna()
    mean_crime = crime_num.groupby('State').mean()
    top15_highest = mean_crime.sort_values(by=['Violent Crime'],
                                           ascending=False).head(15)
    edu = edu[['State', "Percent of adults with a bachelor's degree or higher"]]
    mean_edu = edu.groupby('State').mean()
    crime_education_highest = top15_highest.merge(mean_edu,
                                                  left_on='State', right_on='State', how='left')
    sns.relplot(data=crime_education_highest, x="Percent of adults with\
                a bachelor's degree or higher", y='Violent Crime', style='State', hue='State')
    plt.title("Fifteen States with Highest Number of Crime")
    plt.xlabel("Percent of adults with a bachelor's degree or higher")
    plt.ylabel("Number of Violent Crime")
    plt.savefig("Highest_fifteen_states.png")


def plot_15_highest_reg(crime_num, edu):
    crime_num = crime_num[['State', 'Violent Crime']].dropna()
    mean_crime = crime_num.groupby('State').mean()
    top15_highest = mean_crime.sort_values(by=['Violent Crime'],
                                           ascending=False).head(15)
    edu = edu[['State', "Percent of adults with a bachelor's degree or higher"]]
    mean_edu = edu.groupby('State').mean()
    crime_education_highest = top15_highest.merge(mean_edu,
                                                  left_on='State', right_on='State', how='left')
    sns.jointplot(x="Percent of adults with a bachelor's degree or higher",
                  y='Violent Crime', data=crime_education_highest, kind="reg")
    plt.xlabel("Percent of adults with a bachelor's degree or higher")
    plt.ylabel("Number of Violent Crime")
    plt.savefig("Highest_fifteen_states_reg.png")

def plot_edu_crime_map(crime_num, edu, country):
    education_merge = country.merge(edu, left_on='NAME', right_on='State', how='left')
    education_merge = education_merge[["State", "geometry",
                                     "Percent of adults with a bachelor's degree or higher"]]
    edu_by_state = education_merge.dissolve(by='State', aggfunc='mean')
    fig, [ax1, ax2] = plt.subplots(2, figsize=(20, 20))
    edu_by_state.plot(column="Percent of adults with a bachelor's degree or higher",
                      legend=True, ax=ax1)
    crime_merge = country.merge(crime_num, left_on='NAME', right_on='State', how='left')
    crime_merge = crime_merge[["State", "geometry", "Violent Crime"]]
    crime_by_state = crime_merge.dissolve(by='State', aggfunc='mean')
    crime_by_state.plot(column="Violent Crime", legend=True, ax = ax2)
    ax1.set_title("Education Level across the US")
    ax2.set_title("Number of Violent Crimes in different States")
    plt.savefig('education_crime_comparison.png')


def plot_edu_map(edu, country):
    education = country.merge(Education, left_on='NAME', right_on='State', how='left')
    education = education[["State", "geometry",
                           "Percent of adults with a bachelor's degree or higher"]]
    edu_by_state = education.dissolve(by='State', aggfunc='mean')
    fig, ax = plt.subplots(1, figsize=(10, 10))
    edu_by_state.plot(column="Percent of adults with a bachelor's degree or higher",
                      legend=True, ax=ax)
    plt.title("Education Level by State")
    plt.savefig('education_by_state.png')


def main():
    country = gpd.read_file("gz_2010_us_040_00_5m.json")
    country = country[(country['NAME'] != 'Alaska') & (country["NAME"] != 'Hawaii')]
    country['NAME'] = country['NAME'].str.upper()
    crime = pd.read_csv('Crime Data USA 2019.csv')
    Education = pd.read_excel('Education 2014-2018.xls')
    Education = Education[(Education['State'] != 'Alaska')]
    Education['State'] = Education['State'].str.upper()
    plot_15_lowest(crime, Education)
    plot_15_lowest_reg(crime, Education)
    plot_15_highest(crime, Education)
    plot_15_highest_reg(crime, Education)
    plot_edu_map(edu, country)
    plot_edu_crime_map(crime, edu, country)


if __name__ == '__main__':
    main()
