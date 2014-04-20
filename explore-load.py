import os
import sklearn as sk
import pandas as pd
import numpy as np

# modeling
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score
from sklearn.grid_search import GridSearchCV

from sklearn.linear_model import Ridge

# Module versions.
print 'scikit-learn version:', sk.__version__
print 'pandas version:', pd.__version__

cwd = os.getcwd()
p = os.path.dirname(cwd)
data_dir_path = os.path.join(p, 'GES12')
input_file_path = os.path.join(data_dir_path, 'PERSON.TXT')

input_data = pd.read_csv(input_file_path, delimiter='\t')

sorted_input_data = sorted(input_data.columns)
# print sorted_input_data

# Retrieve severity of injury from input data.
# a is type <class 'pandas.core.series.Series'>
# Pandas data structures - Series = 1-D labeled array
# capable of holding any data type including Python objects.
a = input_data.INJSEV_IM.value_counts()
# print a
# print type(a)

# Removing top severity (6) from data.
# Severity 6 = 4 cases.
input_data = input_data[input_data.INJSEV_IM != 6]

for column_name in input_data.columns:
    n_nans = input_data[column_name].isnull().sum()
    if n_nans > 0:
        print column_name, n_nans

# Drop unnecessary data columns.
print input_data.shape
data = input_data[~input_data.MAKE.isnull()]
discarded = data.pop('INJ_SEV')
target = data.pop('INJSEV_IM')
print data.shape

target = (target == 4).astype('float')

# Begin modeling
# Allocate training and testing datasets
xtrain, xtest, ytrain, ytest = sk.cross_validation.train_test_split(
    data.values, target.values, train_size=0.5)

# Ordinary Least Squares (OLS) - fits a linear model
linreg = LinearRegression()
linreg.fit(xtrain, ytrain)

linreg_prediction = linreg.predict(xtest)

# Predict area under curve (AUC)
linreg_performance = roc_auc_score(ytest, linreg_prediction)
print 'OLS AUC = {}'.format(linreg_performance)

# Ridge Regression
# '[Imposes] a penalty on the size of coeffficients'.
# This addresses some of the problems of OLS.
ridge = GridSearchCV(Ridge(),
                     {'alpha': np.logspace(-10, 10, 10)})
ridge.fit(xtrain, ytrain)
ridge_prediction = ridge.predict(xtest)
ridge_performance = roc_auc_score(ytest, ridge_prediction)
print 'Ridge AUC = {}'.format(ridge_performance)
