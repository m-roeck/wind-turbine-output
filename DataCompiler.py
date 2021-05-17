import pandas as pd
import numpy as np

#Import 12 months of data. 
counter = 1
while counter < 13:
    exec('df{} = pd.read_csv("/Users/mroeck/Desktop/Coding/Scripts/Wind Performance/Raw Wind Data/{}.csv")'.format(counter, counter))
    counter = counter + 1

#Concatenate
frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]
compiled = pd.concat(frames, ignore_index=True)

#Datetime Conversion
compiled['Datetime'] = pd.to_datetime(compiled['Date and Time'])
compiled = compiled.set_index('Datetime')
#compiled = compiled.sort_values(by="Datetime")

#Resampling (15M, 30M, H)
compiled = compiled.resample('H').mean()

#Replace NaN with last viable value (Sep. 2018 was missing data). Method fills forward with the last non-NaN value.
compiled.fillna(method='backfill', inplace=True)

#Round Values
compiled = compiled.round(decimals=0)

#Export to CSV
compiled.to_csv("/Users/mroeck/Desktop/Coding/Scripts/Wind Performance/Raw Wind Data/compiled.csv")



