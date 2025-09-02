from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

app = FastAPI()

# Simulated demand data
dates = pd.date_range("2025-01-01", periods=30)
actual = np.random.randint(80, 120, size=len(dates))

# Train model for forecasting
X = np.arange(len(dates)).reshape(-1, 1)
y = actual
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)
forecast = model.predict(X)

# Create forecast DataFrame
forecast_df = pd.DataFrame({
    "date": dates,
    "actual": actual,
    "forecast": forecast.astype(int)
})

# Simulated warehouse stock
warehouse_data = pd.DataFrame({
    "warehouse": ["A", "B", "C"],
    "stock": [500, 300, 700],
    "stockouts": [2, 5, 1]
})

# Simulated CO₂ emissions
emissions_data = pd.DataFrame({
    "date": dates,
    "emissions": np.random.uniform(50, 150, size=len(dates)).round(2)
})


@app.get("/")
def root():
    return {"message": "Supply Chain API is running 🚀"}


@app.get("/forecast")
def get_forecast():
    return forecast_df.to_dict(orient="records")


@app.get("/warehouse")
def get_warehouse():
    return warehouse_data.to_dict(orient="records")


@app.get("/emissions")
def get_emissions():
    return emissions_data.to_dict(orient="records")
