import numpy as np
from sklearn.datasets import make_regression
import pandas as pd
import matplotlib.pyplot as plt

age, income = make_regression(1000, 1, 1, noise=5.3, random_state=42)
age = age.reshape((1000,))
age = np.log(age * age + 1) * 17 + 20
age = np.floor(age)
income = income * income * 6 + 500
df = pd.DataFrame({'Age': age, 'Income': income})
print('Max age {0}, min age: {1}'.format(age.max(), age.min()))
print('Max income {0}, min income: {1}'.format(income.max(), income.min()))
print(df[0:10])
plt.plot(age, income, 'o')
plt.show()
