# see documentation at https://pandas.pydata.org/pandas-docs/version/0.22.0/r_interface.html
#

# load pandas for R to pandas conversion
import pandas as pd

# import rpy2 functions
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

# import R packages, if R code is only prompted once and as a block it may
# also be desired to source an R script
base = importr('base')
campnet = importr('CampNetworkSimulator')

# simulate network and obtain results as R dataframe
obj = campnet.net_simulate()
results = base.as_data_frame(obj[3])#['network_simulation_object'])

# convert R df to pandas df
with localconverter(ro.default_converter + pandas2ri.converter):
  pd_from_r_df = ro.conversion.rpy2py(results)

#check the pandas conversion worked
print(pd_from_r_df)
print(type(pd_from_r_df))
print(pd_from_r_df.shape)




