import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_excel('processed_data.xlsx')
X, y = df.drop(['price'], axis=1), df.price
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
model = LinearRegression()
model.fit(X_train, y_train)


def predict_flat_cost(flat_data):
    pred_cost = model.predict(pd.DataFrame([flat_data]))
    return int(pred_cost[0])
