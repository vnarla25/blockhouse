import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Generate Synthetic Data
np.random.seed(42)
n = 100  # Number of time intervals

timestamps = pd.date_range(start='2025-01-01', periods=n, freq='T')
prices = np.cumsum(np.random.randn(n) * 0.5 + 100)  # Synthetic price series
volumes = np.random.randint(100, 1000, size=n)  # Synthetic volume series

data = pd.DataFrame({'Timestamp': timestamps, 'Price': prices, 'Volume': volumes})
data['VWAP'] = (data['Price'] * data['Volume']).cumsum() / data['Volume'].cumsum()  # VWAP calculation

# Step 2: TWAP Execution Simulation
total_volume = 10000
num_trades = 10
trade_volume = total_volume // num_trades
execution_prices = []

for i in range(num_trades):
    interval = n // num_trades
    price = data['Price'].iloc[i * interval:(i + 1) * interval].mean()
    execution_prices.append(price)

execution_prices = np.array(execution_prices)
execution_timestamps = timestamps[::interval][:num_trades]

# Step 3: Metrics Calculation
executed_price = execution_prices.mean()
vwap_price = data['VWAP'].iloc[-1]
execution_cost = executed_price - vwap_price

expected_price = data['Price'].mean()
slippage = executed_price - expected_price

# Step 4: Output Metrics
print("Execution Metrics")
print(f"Executed Price: {executed_price:.2f}")
print(f"VWAP Price: {vwap_price:.2f}")
print(f"Execution Cost: {execution_cost:.2f}")
print(f"Expected Price: {expected_price:.2f}")
print(f"Slippage: {slippage:.2f}")

# Plotting for visualization
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['Price'], label='Price')
plt.scatter(execution_timestamps, execution_prices, color='red', label='TWAP Execution')
plt.plot(data['Timestamp'], data['VWAP'], label='VWAP', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('TWAP Execution Simulation')
plt.legend()
plt.grid(True)
plt.show()
