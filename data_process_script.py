import pandas as pd

# Load CSV file into a DataFrame
df = pd.read_csv('2016_General_reg.csv')

# prompt: get only data of 7 columns
dfSubSection = df.iloc[:,0:7]

i = 0
data = []
listOfDataDict = []
startCapture = False
for row in dfSubSection.iterrows():
  if row[1][0] == 'Precinct':
    startCapture = True
  if startCapture:
    data.append(pd.Series(row[1]).tolist()) # Convert tuple to DataFrame row object
    i+=1
  if i == 26: # We have total 26 rows which contain original data
    i = 0 # Reset Counter
    dataDict = {}
    dataDict['Precinct_Num'] = int(data[1][0]) # Get Precinct Number
    dataDict['Precinct_name'] = data[1][1] # Get Precinct Name
    # Iterate over first and last row to get 'Total', 'Dems', 'Reps', 'NPA', 'Other'
    for key, value in zip(data[0][2:], data[-1][2:]):
      dataDict[key] = int(value.replace(',', ''))

    # Now iterate over rest of data to get remaining columns
    # data[2:-2]
    for row in data[2:-1]:
      dataDict[row[1]] = row[2]
    listOfDataDict.append(dataDict)
    data = []
    startCapture = False # Reset flag

# Create a new DataFrame from the list of dictionaries
df_new = pd.DataFrame(listOfDataDict)

# Set the index of the DataFrame to the 'Precinct_Num' column
df_new = df_new.set_index('Precinct_Num')

# Save the DataFrame to a new CSV file
df_new.to_csv('MDC_2016_reg.csv')

