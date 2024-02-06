import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from db_admin import DBAdmin

db_admin = DBAdmin()
data = db_admin.get_info()
df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))

# Preprocess data
df['Price'] = pd.to_numeric(df['Price'].replace('Price on request', np.nan)
                            .replace(',', '', regex=True))
df = df.dropna(subset=['Price'])
df['Space'] = pd.to_numeric(df['Space'])

# Scatter plot
plt.scatter(df['Space'], df['Price'], marker='o', color='blue',
            label='Actual Data')

# Linear Regression
X = df[['Space']]
y = df['Price']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=42)

# Fit linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict prices
y_pred = model.predict(X_test)

# Plot regression line
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear Regression')

formatter = FuncFormatter(lambda x, _: "{:,}".format(int(x)))
plt.gca().yaxis.set_major_formatter(formatter)

plt.title('Price vs Space with Linear Regression')
plt.xlabel('Size')
plt.ylabel('Price')
plt.legend()
plt.show()
