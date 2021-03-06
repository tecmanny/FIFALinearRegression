# -*- coding: utf-8 -*-
"""FIFA Linear Regression

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FFeoQt8qGTRY0fH8x5k4xOdb_xIFhPzV

J. Manuel Garcia FIFA Player Potential Predictor

Import necessary libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import linear_model 
from scipy.stats import skew
import numpy as np
# %matplotlib inline

"""Get access to our google drive folders"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/MyDrive/IA'
!ls

"""Dataset visualization"""

dataFIFA = pd.read_csv('CompleteDatasetFIFA.csv')
dataFIFA.info()

"""Dataset correlations"""

dataFIFA.corr()

"""By hand implementation"""

class Lrbh():
  def __init__(self, X, y):
    self.learningR = 0.03
    self.epochs = 1500
    self.n_samples = len(y)
    self.n_features = np.size(X, 1)
    
  
  # Data Normalization
    self.X = np.hstack((np.ones((self.n_samples, 1)), (X - np.mean(X, 0)) / np.std(X, 0)))
    self.y = y[:,np.newaxis]

    self.params = np.zeros((self.n_features + 1, 1))

  ## Fit model
  def fit(self):
    for i in range(self.epochs):
      self.params = self.params - (self.learningR/self.n_samples) * self.X.T @ (self.X @ self.params - self.y)
      
    self.intercept_ = self.params[0]
    self.coef_ = self.params[1:] 

    return self

  # Training
  def score(self, X, y):
    if X is not None:
      n_samples = np.size(X, 0)
      X = np.hstack((np.ones((n_samples, 1)), (X - np.mean(X, 0)) / np.std(X, 0)))
    else:
      X = self.X
    
    if y is not None:
      y = y[:,np.newaxis]
    else:
      y = self.y

    hyp = X @ self.params
    
    return 1 - (((y - hyp)**2).sum() / ((y - y.mean())**2).sum())
   
    
  
  def predict(self, X):
    n_samples = np.size(X, 0)
    
    return np.hstack((np.ones((n_samples, 1)), (X-np.mean(X, 0)) / np.std(X, 0))) @ self.params
  
  
  def get_params(self):
    return self.params

"""By hand vs Framework results"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import metrics
from sklearn.model_selection import cross_val_score


X = dataFIFA[['Age', 'Overall', 'Acceleration', 'Agility', 'Balance', 'Ball control', 'Reactions', 'Stamina', 'Strength', 'Vision']].to_numpy()
y = dataFIFA.Potential.to_numpy()


X_train, X_test, y_train, y_test, = train_test_split(X, y, test_size=0.3, random_state = 42)

by_hand = Lrbh(X_train, y_train).fit()
framework = LinearRegression().fit(X_train, y_train)



by_hand_training = by_hand.score(None, None)
framework_training = framework.score(X_train, y_train)


by_hand_testing = by_hand.score(X_test, y_test)
framework_testing = framework.score(X_test, y_test)
acc = cross_val_score(framework, X, y)
y_ = by_hand.predict(X_test)

print('Mean Squared Error: %.3f' % np.sqrt(metrics.mean_squared_error(y_test,y_)))
print("------------------")
print('Accuracy Framework in training: %.4f' % framework_training)
print('Accuracy By hand in training: %.4f ' % by_hand_training)
print("------------------")
print('Accuracy Framework in testing: %.4f' % framework_testing)
print('Accuracy By hand: in testing: %.4f ' % by_hand_testing)
print("------------------")
print('Mean Cross Validation Score: %.2f' % np.mean(acc))

"""Visualization of our final model"""

from yellowbrick.regressor import PredictionError, ResidualsPlot

visualizer = PredictionError(framework).fit(X_train, y_train)
visualizer.score(X_test, y_test)
visualizer.poof()

"""Queries"""

print("PLEASE ENTER PLAYER INFORMATION")
Age = float(input("Age "))
Overall = float(input("Overall "))
Acceleration = float(input("Acceleration "))
Agility = float(input("Agility "))
Balance = float(input("Balance "))
Ball_control = float(input("Ball control "))
Reactions = float(input("Reactions "))
Stamina = float(input("Stamina "))
Strength = float(input("Strength "))
Vision = float(input("Vision "))

testpredict = framework.predict([[Age, Overall, Acceleration, Agility, Balance, Ball_control, Reactions, Stamina, Strength, Vision]])
print("Your player potential is: %.17f" % testpredict)