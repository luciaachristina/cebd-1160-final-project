import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

os.makedirs('figures',  exist_ok=True)

from sklearn.datasets import load_diabetes


diabetes_dict = load_diabetes()

diabetes_df = pd.DataFrame(data=np.c_[diabetes_dict.data, diabetes_dict.target], columns=diabetes_dict.feature_names + ['target'])
diabetes_df.rename({'bp': 'Blood Pressure', 'bmi': 'Body Mass Index', 's1': 'Total Cholesterol', 's2': 'LDL Cholesterol', 's3': 'HDL Cholesterol', 's4': 'TCH', 's5': 'LTG', 's6': 'Glucose', 'target': 'Diabetes Progression'}, axis=1, inplace=True)


#Creating figures to better visualize the dataset (heatmap)
fig, axes = plt.subplots(figsize=(8,8))
sns.heatmap(diabetes_df.corr(), annot=True, cmap='bone')
axes.set_xticklabels(diabetes_df.columns, rotation=45)
axes.set_yticklabels(diabetes_df.columns, rotation=45)
axes.set_title(f'Visualization of potential correlations')
plt.tight_layout()
plt.savefig('figures/heatmap_visualization.png', dpi=300)
plt.show()
plt.clf()


#Plotting BMI & BP vs Diabetes Progression to demonstrate the correlation with BMI + Progression, but that BP (could have been any other column) does not correlate
plt.style.use("ggplot")

fig, axes = plt.subplots(1, 1, figsize=(8, 8))
axes.scatter(diabetes_df['Diabetes Progression'], diabetes_df['Body Mass Index'], s=(diabetes_df['Blood Pressure']*50) ** 4,
             label=f'Diabetes Progression compared to BMI with BP level', color='slategrey', marker='o', edgecolors='ghostwhite', alpha=0.8)

axes.set_xlabel(f'Diabetes Progression')
axes.set_ylabel(f'Body Mass Index')
axes.set_title(f'Diabetes Progression, Body Mass Index and BP (size)')


axes.legend()
plt.tight_layout()
plt.savefig(f'figures/multiplot_scatter_bp_size.png', dpi=300)
plt.show()



#Defining variables to keep (or drop)

diabetes_df.drop(['age', 'sex', 'Blood Pressure', 'Total Cholesterol', 'LDL Cholesterol', 'HDL Cholesterol', 'TCH', 'LTG', 'Glucose'], axis=1, inplace=True)

x = diabetes_df.drop('Diabetes Progression', axis=1)
y = diabetes_df['Diabetes Progression']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=5)


# Chosen Regression Model

# GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
gradient = GradientBoostingRegressor()
gradient.fit(x_train, y_train)

predicted_values = gradient.predict(x_test)


sns.set(palette="cividis")

# Plotting the difference between real and predicted values
sns.scatterplot(y_test, predicted_values)
plt.plot([0, 350], [0, 350], '--')
plt.xlabel('Real Value')
plt.ylabel('Predicted Value')
plt.title('Real vs Predicted Values (R^2 = 0.2751)')
plt.savefig(f'figures/real_vs_predict.png', dpi=300)
plt.show()

# Plotting the residuals (scatter) : error between the real and predicted values
residuals = y_test - predicted_values
sns.scatterplot(y_test, residuals)
plt.plot([350, 0], [0, 0], '--')
plt.xlabel('Real Value')
plt.ylabel('Residual (difference)')
plt.title('Real Values vs Residuals')
plt.savefig(f'figures/residuals_scatter.png', dpi=300)
plt.show()

# Plotting distribution of residuals
sns.distplot(residuals, bins=30, kde=False)
plt.plot([0, 0], [50, 0], '--')
plt.title('Residual (difference) Distribution')
plt.savefig(f'figures/residuals_distribution.png', dpi=300)
plt.show()



print(f"METRICS FROM A GRADIENT BOOSTING REGRESSION (GBR)")

from sklearn import metrics
print(f"GBR - MAE error(avg abs residual): {metrics.mean_absolute_error(y_test, predicted_values)}")
print(f"GBR - MSE error: {metrics.mean_squared_error(y_test, predicted_values)}")
print(f"GBR - RMSE error: {np.sqrt(metrics.mean_squared_error(y_test, predicted_values))}")
print(f"GBR - R2 Score: {metrics.r2_score(y_test, predicted_values)}")



