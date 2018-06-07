import pandas as pd
import numpy as np

import statsmodels.formula.api as smf

data = pd.read_csv('bond_data.csv')
est=smf.ols(formula='Dnvaltrd~',data=data).fit()
