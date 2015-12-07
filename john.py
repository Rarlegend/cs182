from pandas import *
import numpy as np
from sklearn.grid_search import GridSearchCV
import sklearn.cross_validation as cv
import sklearn.metrics as metrics
from sklearn.svm import l1_min_c
from sklearn.linear_model import Lasso, LassoCV, LogisticRegression
import scipy.linalg as la
from math import pi
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from patsy import dmatrix
import re
import os
import math
#from tdm_df import tdm_df

x = [[1,2],[2,3],[4,5],[8,9]]
y = [1,4,6,7]

lasso_model = LassoCV(cv=3)
lasso_fit = lasso_model.fit(x, y)


plt.plot(-np.log(lasso_fit.alphas_), np.sqrt(lasso_fit.mse_path_), alpha = .5)
plt.plot(-np.log(lasso_fit.alphas_), np.sqrt(lasso_fit.mse_path_).mean(axis = 1), 
         lw = 2, color = 'black')
plt.ylim(0, 60)
plt.xlim(0, np.max(-np.log(lasso_fit.alphas_)))
plt.title('Lasso regression RMSE')
plt.xlabel(r'$-\log(\lambda)$')
plt.ylabel('RMSE (and avg. across folds)')