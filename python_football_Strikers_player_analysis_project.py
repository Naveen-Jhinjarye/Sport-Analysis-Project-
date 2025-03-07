# -*- coding: utf-8 -*-
"""Python Football Player Analysis Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1x8rhz0wDAqqpZhlcPsd3kVnc4r2rDWCX

**Football Player  Analysis Project**

**Load File**
"""

from google.colab import files

# Upload the file
print("Please upload your Excel file:")
uploaded = files.upload()

# Automatically handle the uploaded file (no need to input file name manually)
print("\nUploaded file(s) have been successfully uploaded!")

"""**Load Require pckages**"""

import pandas as pd
import numpy as np

"""**Load Datasets**"""

sport = pd.read_excel('Strikers_performance.xlsx')
sport.head()

"""#Data Cleaning

##Missing Values
"""

missing_values = sport.isnull().sum()
print("Missing Values")
missing_values

from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy = 'median')
imputer.fit(sport[['Movement off the Ball']])
sport[['Movement off the Ball']] = imputer.transform(sport[['Movement off the Ball']])

imputer = SimpleImputer(strategy ='median')
imputer.fit(sport[['Big Game Performance']])
sport[['Big Game Performance']] = imputer.transform(sport[['Big Game Performance']])

imputer = SimpleImputer(strategy = 'median')
imputer.fit(sport[['Penalty Success Rate']])
sport[['Penalty Success Rate']] = imputer.transform(sport[['Penalty Success Rate']])

missing_values = sport.isnull().sum()
print("Missing Values")
missing_values

"""#Data Types"""

sport.dtypes

variables = ['Goals Scored', 'Assists',
             'Shots on Target',
             'Movement off the Ball',
             'Hold-up Play',
             'Aerial Duels Won',
             'Defensive Contribution',
             'Big Game Performance',
             'Impact on Team Performance',
             'Off-field Conduct']
for var in variables:
    sport[var] = sport[var].astype('int64')

sport.dtypes

sport.dtypes

"""#Exploratory Data Analysis

##Perform Descriptive Data analysis
"""

round(sport.describe(), 2)

sport.describe(include=['object'])

round(sport.describe(), 2)

import matplotlib.pyplot as plt
import seaborn as sns

"""##Perform Percentage Analysis"""

perc_Footedness = sport['Footedness'].value_counts()
perc_Footedness

perc_Footedness_1 = perc_Footedness / len(sport['Footedness']) * 100
perc_Footedness_1

plt.figure(figsize = (6, 4))
perc_Footedness_1.plot(kind = 'pie', autopct = '%1.2f%%')
plt.title('Percentage of strikers by footedness')
plt.ylabel('')
plt.show()

"""###What is the distribution of players' footedness across different nationalities?"""

Count_plot = pd.crosstab(sport['Footedness'],sport['Nationality'])
Count_plot

plt.figure(figsize = (12, 4))
Count_plot.plot(kind = 'bar', stacked = False)
plt.title('Right vs. Left-Footed Strikers Across Different Nationalities')
plt.legend(loc = 'upper right')
plt.xlabel('Type Of Footedness')
plt.ylabel('Footed Value')
plt.show()

plt.figure(figsize = (12, 4))
sns.countplot(x = 'Footedness', hue = 'Nationality', data = sport)
plt.title('Right vs. Left-Footed Strikers Across Different Nationalities')
plt.xlabel('Type Of Footedness')
plt.ylabel('Footed Value')
plt.show()

""" ### Determine which nationality strikers have the highest average number of goals scored."""

grouped_var = sport.groupby('Nationality') ['Goals Scored'].mean().sort_values(ascending = False)
grouped_var

"""###What is the average conversion rate for players based on their footedness?"""

grouped_var_2  = sport.groupby('Footedness') ['Conversion Rate'].mean().sort_values(ascending = False)
grouped_var_2

"""###Create A Correlation Matrix With A Heatmap"""

num_variables = sport.select_dtypes(include = ['number']).columns

correl_matrix = round(sport[num_variables].corr(), 3)
correl_matrix

plt.figure(figsize = (18, 8))
sns.heatmap(correl_matrix, annot = True)
plt.title('Correlation Matrix')
plt.show()

"""#Statistical Test

### Find whether there is any significant difference in consistency rates among strikers from various nationality
"""

from scipy.stats import shapiro

test_columns = ['Consistency']
shapiro_results = {}
for column in test_columns:
  stats, p_value = shapiro(sport[column])
  shapiro_results[column] = round(p_value, 3)
shapiro_results

from scipy.stats import levene

from scipy.stats import f_oneway

Space = sport.query('Nationality == "Spain"')['Consistency']
France = sport.query('Nationality == "France"')['Consistency']
Germany = sport.query('Nationality == "Germany"')['Consistency']
Brazil = sport.query('Nationality == "Brazil"')['Consistency']
England = sport.query('Nationality == "England"')['Consistency']

test_levene = levene(Space, France, Germany, Brazil, England)
print('P-value', round(p_value, 3))

test_anova, p_value =f_oneway(Space, France, Germany, Brazil, England)
print('P-value', round(p_value, 3))
if p_value < 0.05:
  print('Reject the null hypothesis')
else:
  print('Fail to reject the null hypothesis')

"""### Check if there is any significant correlation between strikers' Hold-up play and consistency rate"""

from scipy.stats import pearsonr

test_columns_2 = ['Hold-up Play']
shapiro_results = {}
for column in test_columns_2:
  stats, p_valye = shapiro(sport[column])
  shapiro_results[column] = round(p_value, 3)
shapiro_results

Play = sport['Hold-up Play']
Consistency = sport['Consistency']

corr, p_value = pearsonr(Play, Consistency)
print('Correlation_Coefficent', round(corr, 3))
print('P-value', round(p_value, 3))
if p_value < 0.05:
  print('Reject the null hypothesis')
else:
  print('Fail to reject the null hypothesis')

"""### Check if strikers' hold-up play significantly influences their consistency rate"""

import statsmodels.api as sm

x = sport['Hold-up Play']
y = sport['Consistency']

x_constant = sm.add_constant(x)
model = sm.OLS(y, x_constant).fit()
print(model.summary())

"""#Feature Engineering

### Create a new feature - Total contribution scor
"""

sport['Total Contribution Score_3'] = (sport['Goals Scored'] + sport['Assists'] + sport['Shots on Target'] + sport['Aerial Duels Won'] + sport['Defensive Contribution'] + sport['Big Game Performance'] + sport['Consistency'] + sport['Dribbling Success'])
sport.head()

"""### Encode the Footedness and marital status by LabelEncoder"""

from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()  # LabelEncoder ka object banao
sport['Marital Status'] = encoder.fit_transform(sport['Marital Status'])  # Encoding apply karo

sport  # Updated dataframe dekho

encoder = LabelEncoder()  # LabelEncoder ka object banao
sport['Footedness'] = encoder.fit_transform(sport['Footedness'])  # Encoding apply karo

sport  # Updated dataframe dekho

"""### Create the dummies for Nationality and add with the data"""

dummies = pd.get_dummies(sport['Nationality'])
sport = pd.concat([sport, dummies], axis = 1)
sport = sport.drop('Nationality', axis = 1)
sport.head()



# Sirf nationality ke dummies columns ko 0-1 mein convert karna
sport[['Brazil', 'England', 'France', 'Germany', 'Spain']] = sport[['Brazil', 'England', 'France', 'Germany', 'Spain']].astype(int)

"""#Cluster Analysis

### Perform KMeans clsutering
"""

from sklearn.cluster import KMeans

x = sport.drop('Striker_ID', axis=1)  # ID Column Drop Kiya

wcss = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init='auto')
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)  # WCSS Score Store Kiya

# Elbow Method Graph Plot
plt.plot(range(1, 15), wcss, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method for Optimal Clusters')
plt.show()

final_km = KMeans(n_clusters = 2)
final_km.fit(x)

# Generating labels
labels = final_km.labels_
labels

sport['Clusters'] = labels
sport.head()

round(sport.groupby('Clusters')['Total Contribution Score_3'].mean(), 2)

mapping = {0:'Best Strikers', 1 : 'Regular Strikers'}
sport['Cluster_Types'] = sport['Clusters'].map(mapping)

sport = sport.drop('Clusters', axis = 1)
sport.head()

sport.columns

"""#Data Preprocessing ML

###New Feature Mapping
"""

mapping = {'Best Strikers': 1, 'Regular Strikers': 0}
sport['Cluster_Types'] = sport['Cluster_Types'].map(mapping)

sport.head()

"""###Selecting Features"""

x = sport.drop(['Striker_ID', 'Cluster_Types'], axis = 1)
y = sport['Cluster_Types']

"""###Standard Scaler Features"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaled_x = scaler.fit_transform(x)
scaled_x

"""###Train Test Split"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(scaled_x, y, test_size = 0.2, random_state = 42)

"""# Predictive Classification Analytics

### Build a logistic regression machine learning model to predict strikers type
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

model = LogisticRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy * 100, '%')

conff_matrix = confusion_matrix(y_test, y_pred)

plt.figure(figsize = (10,8))
sns.heatmap(conff_matrix, annot = True, fmt = "d", cmap = "Blues" )
plt.title('Confusion Matrix for LGR model')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

"""#Thank You"""