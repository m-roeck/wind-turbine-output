import pandas as pd
import numpy as np
from WindTurbineOutput import *

counter = int(0)

#retrieve Hub Height
HubHeight = int(input("Enter the hub height of the turbine (m): "))

#retrieve actual air density (kg/m3)
rho = float(input("Enter the actual air density (kg/m3): "))

#retrieve export pathname
pathname = input("Enter the pathname for results: ")

#import Wind Speeds
WindSpeed = pd.read_csv("/Users/mroeck/Desktop/Coding/Scripts/Wind Performance/Raw Wind Data/compiled_speeds.csv")

# drop dispensible columns
if HubHeight <= 40:
    WindSpeed.drop(columns=WindSpeed.columns[[2,3,4,5,6,7,8,9,10]], axis=1, inplace=True)
    WindSpeed['40_2'] = WindSpeed['40']
elif HubHeight > 40 and HubHeight <= 50:
    WindSpeed.drop(columns=WindSpeed.columns[[3,4,5,6,7,8,9,10]], axis=1, inplace=True)
elif HubHeight > 50 and HubHeight <= 60:
    WindSpeed.drop(columns=WindSpeed.columns[[1,4,5,6,7,8,9,10]], axis=1, inplace=True)
elif HubHeight > 60 and HubHeight <= 80:
    WindSpeed.drop(columns=WindSpeed.columns[[1,2,5,6,7,8,9,10]], axis=1, inplace=True)
elif HubHeight > 80 and HubHeight <= 100:
    WindSpeed.drop(columns=WindSpeed.columns[[1,2,3,6,7,8,9,10]], axis=1, inplace=True)
elif HubHeight > 100 and HubHeight <= 120:
    WindSpeed.drop(columns=WindSpeed.columns[[1,2,3,4,7,8,9,10]], axis=1, inplace=True)
elif HubHeight > 120 and HubHeight <= 140:
    WindSpeed.drop(columns=WindSpeed.columns[[1,2,3,4,5,8,9,10]], axis=1, inplace=True)
elif HubHeight > 140 and HubHeight <= 160:
    WindSpeed.drop(columns=WindSpeed.columns[[1,2,3,4,5,6,9,10]], axis=1, inplace=True)
elif HubHeight > 160 and HubHeight <= 180:
    WindSpeed.drop(columns=WindSpeed.columns[[1,2,3,4,5,6,7,10]], axis=1, inplace=True)
else:
    WindSpeed.drop(columns=WindSpeed.coumns[[1,2,3,4,5,6,7,8]], axis=1, inplace=True)

#create columns
WindSpeed['speed'] = 1

#replace 0's
WindSpeed.replace(to_replace=0, value=1, inplace=True)

#calculate true wind speed
while counter < 8497:
    
    #calculate wind sheer at hub height
    v_1 = int(WindSpeed.iloc[counter, 1])
    v_2 = int(WindSpeed.iloc[counter, 2])
    z_1 = int(WindSpeed.columns[1])
    z_2 = int(WindSpeed.columns[2])
    shear = CalcWindShear(v_1, v_2, z_1,z_2)

    #Calculate Wind Speed at Hub Height
    v_anem = int(WindSpeed.iloc[counter, 1])
    z_anem = int(WindSpeed.columns[1])
    WindSpeed.iloc[counter,3] = CalcHubHeightWindSpeed(v_anem, HubHeight, z_anem, shear)

    counter = counter + 1

print(WindSpeed)

#round && add ceiling
WindSpeed = WindSpeed.round(decimals=0)
WindSpeed['speed'].values[WindSpeed['speed'] > 25] = 25
#Note: Rounding is neccessary for matching, but rounding also mitigates the speed calculation at exact hub height.

###
###Calculating Wind Turbine Output at the Actual Air Density
###

TurbinePerformance = pd.read_csv("/Users/mroeck/Desktop/Coding/Scripts/Wind Performance/Turbines/E-44.csv")
TurbinePerformance['output'] = TurbinePerformance['output'].map(lambda x: ApplyDensityCorrection(x, rho, rho_0=1.225))

WindSpeed = WindSpeed.merge(TurbinePerformance,how='left',on='speed')

WindSpeed.to_csv(pathname)