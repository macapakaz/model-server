import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
utils = rpackages.importr('utils')
devtools = rpackages.importr('devtools')
campnet = devtools.install_github("AIforGoodSimulator/network-model-R-package")


