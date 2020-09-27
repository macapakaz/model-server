import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages

campnet = importr('CampNetworkSimulator')
obj = campnet.net_simulate()

print(obj)
print(type(obj))

# fetch plot using R plotting function
print(campnet.plot_states(obj))
