import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create dummy data for 20MICRONS stock
dates = [datetime(2021, 11, 4) - timedelta(days=i) for i in range(459)]
dates = [d.strftime('%Y-%m-%d') for d in dates]

data = {
    'Unnamed: 0': ['closing_price'] * 1,
    'symbol': ['20MICRONS'] * 1
}

for i, date in enumerate(dates):
    # Just generate some random-ish walk data
    price = 50 + (i * 0.1) + (10 * np.sin(i / 10.0))
    data[date] = [round(price, 2)]

df = pd.DataFrame(data)
df.to_csv('All_Stocks_Data.csv', index=False)
print("Dummy All_Stocks_Data.csv created successfully.")
