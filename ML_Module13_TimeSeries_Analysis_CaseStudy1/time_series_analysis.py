# time_series_analysis.py
# Time series analysis and forecasting using SARIMAX model
# - Load and preprocess data
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt

# Load
df = pd.read_csv("SeaPlaneTravel.csv")
df['Month'] = pd.to_datetime(df['Month'], errors='coerce')
df = df.sort_values('Month').set_index('Month')

# detect passenger column and reindex to monthly
pass_col = next((c for c in df.columns if 'passeng' in c.lower() or 'pass' in c.lower()), df.columns[0])
full_idx = pd.date_range(start=df.index.min(), end=df.index.max(), freq='MS')
df = df.reindex(full_idx)
df[pass_col] = df[pass_col].astype(float).interpolate().ffill().bfill()
df = df.rename(columns={pass_col: 'passengers'})

# Train/test split
n_test = 12
train = df.iloc[:-n_test]
test = df.iloc[-n_test:]

# Fit SARIMAX
model = SARIMAX(train['passengers'], order=(1,1,1), seasonal_order=(1,1,1,12),
                enforce_stationarity=False, enforce_invertibility=False)
res = model.fit(disp=False)

# Forecast and evaluate
pred_test = res.get_forecast(steps=n_test)
pred_test_mean = pred_test.predicted_mean
mape = mean_absolute_percentage_error(test['passengers'], pred_test_mean)
print("MAPE:", mape)

# Forecast next 12 months
steps_future = 12
pred_future = res.get_forecast(steps=n_test + steps_future)
pred_future_mean = pred_future.predicted_mean
pred_future_ci = pred_future.conf_int()
pred_index = pred_future_mean.index
forecast_df = pd.DataFrame({
    'forecast': pred_future_mean,
    'lower_ci': pred_future_ci.iloc[:,0],
    'upper_ci': pred_future_ci.iloc[:,1]
}, index=pred_index)
future_df = forecast_df.tail(steps_future).reset_index().rename(columns={'index':'Month'})
future_df['Month'] = future_df['Month'].dt.strftime('%Y-%m-%d')
future_df.to_csv('seaplane_forecast.csv', index=False)
