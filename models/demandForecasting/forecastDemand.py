from models.demandForecasting.previousData import getProductIds,getDataFrame
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import datetime

def getForecasts():
    # Get the current year and month
    now = datetime.datetime.now()
    current_year_month = now.strftime('%Y-%m')
    
    product_ids=getProductIds()
    data_frame=getDataFrame()

    # Filter the DataFrame to exclude rows with the current month
    data_frame = data_frame[data_frame['year_month'] != current_year_month]

    # Split summary table into separate tables for each product
    product_tables = {}
    for product_id in product_ids:
        product_table = data_frame[['year_month', product_id]].rename(columns={product_id: 'sales'})
        product_table['year_month'] = pd.to_datetime(product_table['year_month'])
        product_table.set_index('year_month', inplace=True)
        product_tables[product_id] = product_table

    # Define function to fit ARIMA model and forecast sales for next month
    def forecast_sales(product_table):
        # Resample to monthly frequency and fill missing months with NaN values
        product_table = product_table.resample('M').sum()
        product_table = product_table.fillna(np.nan)

        # Split into training and testing sets
        train = product_table[:-1]
        test = product_table[-1:]

        # Fit ARIMA model to training data
        model = ARIMA(train, order=(1,1,1))
        model_fit = model.fit()

        # Forecast sales for next month and round to nearest integer
        forecast = round(model_fit.forecast(steps=1)[0])

        return forecast

    # Loop over product tables and forecast sales for next month
    forecasts = {}
    for product_id, product_table in product_tables.items():
        forecast = forecast_sales(product_table)
        forecasts[product_id] = forecast

    return forecasts    

