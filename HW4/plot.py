from plotly.offline import *
from plotly.graph_objs import *
import numpy as np
import matplotlib.pyplot as plt
init_notebook_mode()
%matplotlib inline

plt.plot([0,1,2,3])
x = np.random.randn(2000)
y = np.random.randn(2000)


iplot([Scatter(x=[1, 2, 3], y=[3, 1, 6])])

import pandas as pd
df = pd.read_csv('https://plot.ly/~etpinard/191.csv')
df.head(1)
