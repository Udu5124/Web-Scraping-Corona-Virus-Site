import requests
import bs4
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
import getpass

# Base URL for the worldometer web page
base_url = 'https://www.worldometers.info/coronavirus/country/us/'


# Take data from website and make it readable using beautifulsoup
results = requests.get(base_url)
soup = bs4.BeautifulSoup(results.text, 'lxml')


# Open file to write the scraped data
with open('top_ten_states_corona_data.csv', 'w') as file:

    # Loop 10 times to extract data for top 10 states affected
    for item in range(2, 12):

        # Replace every '\n' in the extracted data to ','
        row = soup.find_all('tr', {'style': ''})[item].text.replace('\n', ',')

        # Write the row in the file
        file.write(row)
        file.write('\n')

# Read the CSV file created in 'ISO-8859-1' encoding
data = pd.read_csv('top_ten_states_corona_data.csv', encoding = 'ISO-8859-1', delimiter = ',', header = None)

# Drop all columns except the states and affected cases columns
data.dropna(axis = 1, how ='all', inplace = True)
data = data.drop(data.columns[range(3,25)], axis=1)


# Create total cases column as the digits are in seperate columns
# Example: data["total_cases"] = data[3] + data[4]
#          423499 = (423 * 1000) + 499
data.loc[:,[3]] = data.loc[:,[3]] * 1000
data["total_cases"] = data[3] + data[4]

# Drop data[3] and data[4] columns
data = data.drop(data.columns[[1,2]], axis=1)

# Renaming the remaining columns
data.columns = ['states','total_cases']

# Put the data from csv file into a data frame3
df = pd.DataFrame(data, columns = ['states','total_cases'])

# Code for Pie chart representation
#explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
#df.plot.pie(labels=df['states'], legend= False, y='total_cases', explode=explode, figsize= (9,8), shadow=True, startangle =180, autopct='%.2f',subplots=True)

# Plotting Bar graph
df.plot.bar(x='states', rot= 0 ,figsize= (16,8), legend= False, title = 'Top 10 states affected by corona in US')
plt.xlabel('Top 10 states affected by corona virus')
plt.ylabel('Total deaths')

# Code for printing values on top of bar graph
for i, v in enumerate(df['total_cases']):
    plt.text(i-0.2, v+(2000), str(v))

# Save the graph as a .png file
plt.savefig('top_10_US_corona_states.png')
plt.show()