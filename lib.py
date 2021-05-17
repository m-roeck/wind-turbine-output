import numpy as np
import pandas as pd

#Calculate Wind Turbine Power Output
#Reference = https://www.homerenergy.com/products/pro/docs/latest/how_homer_calculates_wind_turbine_power_output.html

###
###Calculating Hub Height Wind Speed using Wind Profile Power Law
###

#returns the wind speed at the hub height of the wind turbines (m/s)
#v_anem = the wind speed at anemometer height [m/s]
#z_hub = the hub height of the wind turbine [m]
#z_anem = the anemometer height [m]
#shear = wind shear exponent

def CalcHubHeightWindSpeed(v_anem, z_hub, z_anem, shear):
    return v_anem*(z_hub/z_anem)**shear

###
###Calculate Wind Shear Exponent
###

#returns shear exponent
#v_1 = Velocity at height z_1
#v_2 = Velocity at height z_2
#z_1 = height 1 (lower height)
#z_2 = height 2 (higher height)

def CalcWindShear(v_1, v_2, z_1,z_2):
    return np.log(v_2/v_1)/np.log(z_2/z_1)

###
###Applying Density Correction
###

#returns the wind turbine power output [kW]
#Output_STP = the wind turbine power output at standard temperature and pressure [kW]
#rho = the actual air density [kg/m3]
#rho_0 = the air density at standard temperature and pressure (1.225 kg/m3)

def ApplyDensityCorrection(Output_STP, rho, rho_0=1.225):
    return (rho/rho_0)*Output_STP