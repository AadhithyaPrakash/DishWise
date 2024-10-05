import pandas as pd
import numpy as np
import time
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import requests
from geopy.distance import geodesic

data = pd.read_csv('D:\DISHWISE\DishWise-main\scripts\FINAL.csv')
geo_data = pd.read_csv('D:\DISHWISE\DishWise-main\scripts\location.csv')
data = pd.merge(data, geo_data, how='left', on='District')

le_district = LabelEncoder()
le_commodity = LabelEncoder()
le_variety = LabelEncoder()

data['District_Encoded'] = le_district.fit_transform(data['District'])
data['Commodity_Encoded'] = le_commodity.fit_transform(data['Commodity'])
data['Variety_Encoded'] = le_variety.fit_transform(data['Variety'])


data['Year'] = pd.DatetimeIndex(data['Year']).year
month_name_to_number = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
    'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
    'November': 11, 'December': 12
}

data['Month'] = data['Month_Name'].map(month_name_to_number)
data = data.dropna(subset=['Commodity_Encoded', 'Variety_Encoded', 'District_Encoded', 'Year', 'Month', 'Modal_Price'])

features = ['Commodity_Encoded', 'Variety_Encoded', 'District_Encoded', 'Year', 'Month']
target = 'Modal_Price'

X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model for price prediction
start_train_time = time.time()
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
end_train_time = time.time()
training_time = end_train_time - start_train_time

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

import requests
from geopy.distance import geodesic

# Function to get latitude and longitude using OpenStreetMap Nominatim API
def get_lat_lon_from_district(district_name):
    url = f"https://nominatim.openstreetmap.org/search?q={district_name}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        raise ValueError(f"Could not find coordinates for {district_name}")

# Updated haversine function (using geopy to calculate distance accurately)
def calculate_distance(lat1, lon1, lat2, lon2):
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    return geodesic(loc1, loc2).kilometers  # More accurate calculation using geodesic distance

# Use the API to get latitude and longitude dynamically
def predict_prices(chosen_commodity, chosen_variety, chosen_district, quantity, chosen_month, chosen_year):
    # Fetch latitude and longitude using OpenStreetMap API for the chosen district
    try:
        current_lat, current_lon = get_lat_lon_from_district(chosen_district)
    except ValueError as e:
        print(e)
        return
    
    district_encoded = le_district.transform([chosen_district])[0]
    commodity_encoded = le_commodity.transform([chosen_commodity])[0]
    variety_encoded = le_variety.transform([chosen_variety])[0]

    input_data = pd.DataFrame({
        'Commodity_Encoded': [commodity_encoded],
        'Variety_Encoded': [variety_encoded],
        'District_Encoded': [district_encoded],
        'Year': [chosen_year],
        'Month': [chosen_month]
    })

    predicted_price = rf_model.predict(input_data)[0]
    print(f"Predicted price for {chosen_commodity} in {chosen_district} for {chosen_month}/{chosen_year}: ₹{predicted_price:.2f} per quintal")
    total_cost = (predicted_price / 100) * quantity
    print(f"For {quantity} kg, the estimated total cost is: ₹{total_cost:.2f}")
    
    # Calculate distances from nearby districts
    data['distance'] = data.apply(lambda row: calculate_distance(current_lat, current_lon, row['avg_latitude'], row['avg_longitude']), axis=1)
    
    best_month_data = data[(data['Commodity'] == chosen_commodity) & (data['Variety'] == chosen_variety)]
    
    if not best_month_data.empty:
        best_buy_month_row = best_month_data.groupby('Month')['Modal_Price'].mean().idxmin()
        best_buy_month = pd.to_datetime(f'2023-{best_buy_month_row}-01').month_name()  
        print(f"The best buy month for {chosen_commodity} ({chosen_variety}) is {best_buy_month}.")
    else:
        print("No data available for the selected commodity and variety.")

    nearby_districts = data[(data['Commodity'] == chosen_commodity) &
                             (data['Variety'] == chosen_variety) &
                             (data['District'] != chosen_district)] \
                         .sort_values(by=['distance', 'Modal_Price']).drop_duplicates(subset='District').head(3)
    
    if not nearby_districts.empty:
        print("Nearby districts with best prices:")
        for _, row in nearby_districts.iterrows():
            nearby_district = row['District']
            nearby_distance = row['distance']
            nearby_price = float(row['Modal_Price']) / 100 * quantity
            print(f"- {nearby_district} ({nearby_distance:.2f} km), Price: ₹{nearby_price:.2f} for {quantity} kg")
    else:
        print("No nearby districts found with available data.")


def predict_prices(chosen_commodity, chosen_variety, chosen_district, quantity, chosen_month, chosen_year):
    district_encoded = le_district.transform([chosen_district])[0]
    commodity_encoded = le_commodity.transform([chosen_commodity])[0]
    variety_encoded = le_variety.transform([chosen_variety])[0]

    
    input_data = pd.DataFrame({
        'Commodity_Encoded': [commodity_encoded],
        'Variety_Encoded': [variety_encoded],
        'District_Encoded': [district_encoded],
        'Year': [chosen_year],
        'Month': [chosen_month]
    })

    start_predict_time = time.time()
    predicted_price = rf_model.predict(input_data)[0]
    end_predict_time = time.time()
    prediction_time = end_predict_time - start_predict_time
  
    print(f"Predicted price for {chosen_commodity} in {chosen_district} for {chosen_month}/{chosen_year}: ₹{predicted_price:.2f} per quintal")
    
    
    total_cost = (predicted_price / 100) * quantity
    print(f"For {quantity} kg, the estimated total cost is: ₹{total_cost:.2f}")
    
    current_lat = geo_data[geo_data['District'] == chosen_district]['avg_latitude'].values[0]
    current_lon = geo_data[geo_data['District'] == chosen_district]['avg_longitude'].values[0]

    
    data['distance'] = data.apply(lambda row: haversine(current_lat, current_lon, row['avg_latitude'], row['avg_longitude']), axis=1)

    
    best_month_data = data[(data['Commodity'] == chosen_commodity) &
                            (data['Variety'] == chosen_variety)]
    
    if not best_month_data.empty:
        best_buy_month_row = best_month_data.groupby('Month')['Modal_Price'].mean().idxmin()
        best_buy_month = pd.to_datetime(f'2023-{best_buy_month_row}-01').month_name()  
        print(f"The best buy month for {chosen_commodity} ({chosen_variety}) is {best_buy_month}.")
    else:
        print("No data available for the selected commodity and variety.")

    
    nearby_districts = data[(data['Commodity'] == chosen_commodity) &
                             (data['Variety'] == chosen_variety) &
                             (data['District'] != chosen_district)] \
                         .sort_values(by=['distance', 'Modal_Price']).drop_duplicates(subset='District').head(3)
    
    if not nearby_districts.empty:
        print("Nearby districts with best prices:")
        for _, row in nearby_districts.iterrows():
            nearby_district = row['District']
            nearby_distance = row['distance']
            nearby_price = float(row['Modal_Price'])/100 * (quantity)  # Adjust price according to quantity
            print(f"- {nearby_district} ({nearby_distance:.2f} km), Price: ₹{nearby_price:.2f} for {quantity} kg")
    else:
        print("No nearby districts found with available data.")

# User inputs
chosen_commodity = input("Enter the commodity (e.g., Groundnut): ")
chosen_variety = input("Enter the variety (e.g., Other): ")
chosen_district = input("Enter the district (e.g., Ariyalur): ")
quantity = float(input("Enter the quantity in kg (e.g., 2): "))
chosen_month = int(input("Enter the month as a number (1-12, e.g., 6 for June): "))
chosen_year = int(input("Enter the year (e.g., 2023): "))

# Call the function to predict prices
predict_prices(chosen_commodity, chosen_variety, chosen_district, quantity, chosen_month, chosen_year)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Generate predictions on the test set for evaluation
y_pred_test = rf_model.predict(X_test)

# Calculate performance metrics
mae = mean_absolute_error(y_test, y_pred_test)
mse = mean_squared_error(y_test, y_pred_test)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_test)

# Print performance metrics
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R²): {r2:.2f}")
print(f"Training time: {training_time:.4f} seconds")


import pickle

with open("rf_regressor.H5", "wb") as file:
    pickle.dump(rf_model, file)


import pandas as pd
import numpy as np
import time
import requests  # for API call
from geopy.distance import geodesic  # for accurate distance calculation
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load your data
data = pd.read_csv('FINAL.csv')

# Label encoding the categorical variables
le_district = LabelEncoder()
le_commodity = LabelEncoder()
le_variety = LabelEncoder()

data['District_Encoded'] = le_district.fit_transform(data['District'])
data['Commodity_Encoded'] = le_commodity.fit_transform(data['Commodity'])
data['Variety_Encoded'] = le_variety.fit_transform(data['Variety'])

# Map month names to numbers
month_name_to_number = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
    'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
    'November': 11, 'December': 12
}
data['Month'] = data['Month_Name'].map(month_name_to_number)
data = data.dropna(subset=['Commodity_Encoded', 'Variety_Encoded', 'District_Encoded', 'Year', 'Month', 'Modal_Price'])

# Feature and target selection
features = ['Commodity_Encoded', 'Variety_Encoded', 'District_Encoded', 'Year', 'Month']
target = 'Modal_Price'
X = data[features]
y = data[target]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
start_train_time = time.time()
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
end_train_time = time.time()
training_time = end_train_time - start_train_time

# Function to fetch latitude and longitude using OpenStreetMap Nominatim API
def get_lat_lon_from_district(district_name):
    url = f"https://nominatim.openstreetmap.org/search?q={district_name}&format=json"
    response = requests.get(url)
    data = response.json()
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        raise ValueError(f"Could not find coordinates for {district_name}")

# Updated haversine function (using geopy to calculate distance accurately)
def calculate_distance(lat1, lon1, lat2, lon2):
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    return geodesic(loc1, loc2).kilometers  # Using geodesic distance

# Prediction function incorporating dynamic latitude and longitude fetching
def predict_prices(chosen_commodity, chosen_variety, chosen_district, quantity, chosen_month, chosen_year):
    # Fetch latitude and longitude using OpenStreetMap API for the chosen district
    try:
        current_lat, current_lon = get_lat_lon_from_district(chosen_district)
    except ValueError as e:
        print(e)
        return

    district_encoded = le_district.transform([chosen_district])[0]
    commodity_encoded = le_commodity.transform([chosen_commodity])[0]
    variety_encoded = le_variety.transform([chosen_variety])[0]

    input_data = pd.DataFrame({
        'Commodity_Encoded': [commodity_encoded],
        'Variety_Encoded': [variety_encoded],
        'District_Encoded': [district_encoded],
        'Year': [chosen_year],
        'Month': [chosen_month]
    })

    start_predict_time = time.time()
    predicted_price = rf_model.predict(input_data)[0]
    end_predict_time = time.time()
    prediction_time = end_predict_time - start_predict_time

    print(f"Predicted price for {chosen_commodity} in {chosen_district} for {chosen_month}/{chosen_year}: ₹{predicted_price:.2f} per quintal")

    total_cost = (predicted_price / 100) * quantity
    print(f"For {quantity} kg, the estimated total cost is: ₹{total_cost:.2f}")

    # Calculate distances from nearby districts using fetched coordinates
    data['distance'] = data.apply(lambda row: calculate_distance(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1)

    best_month_data = data[(data['Commodity'] == chosen_commodity) & (data['Variety'] == chosen_variety)]
    
    if not best_month_data.empty:
        best_buy_month_row = best_month_data.groupby('Month')['Modal_Price'].mean().idxmin()
        best_buy_month = pd.to_datetime(f'2023-{best_buy_month_row}-01').month_name()  
        print(f"The best buy month for {chosen_commodity} ({chosen_variety}) is {best_buy_month}.")
    else:
        print("No data available for the selected commodity and variety.")

    nearby_districts = data[(data['Commodity'] == chosen_commodity) &
                             (data['Variety'] == chosen_variety) &
                             (data['District'] != chosen_district)] \
                         .sort_values(by=['distance', 'Modal_Price']).drop_duplicates(subset='District').head(3)

    if not nearby_districts.empty:
        print("Nearby districts with best prices:")
        for _, row in nearby_districts.iterrows():
            nearby_district = row['District']
            nearby_distance = row['distance']
            nearby_price = float(row['Modal_Price']) / 100 * quantity
            print(f"- {nearby_district} ({nearby_distance:.2f} km), Price: ₹{nearby_price:.2f} for {quantity} kg")
    else:
        print("No nearby districts found with available data.")

# User inputs
chosen_commodity = input("Enter the commodity (e.g., Groundnut): ")
chosen_variety = input("Enter the variety (e.g., Other): ")
chosen_district = input("Enter the district (e.g., Ariyalur): ")
quantity = float(input("Enter the quantity in kg (e.g., 2): "))
chosen_month = int(input("Enter the month as a number (1-12, e.g., 6 for June): "))
chosen_year = int(input("Enter the year (e.g., 2023): "))

# Call the function to predict prices
predict_prices(chosen_commodity, chosen_variety, chosen_district, quantity, chosen_month, chosen_year)


