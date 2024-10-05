from flask import Flask, render_template, request, jsonify
import requests
from geopy.distance import geodesic
import pickle

app = Flask(__name__)

# Load the pre-trained model (no training or dataset processing)
model_path = 'D:/DISHWISE/random_forest_model.pkl'
with open(model_path, 'rb') as model_file:
    rf_model = pickle.load(model_file)

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

# Updated haversine function using geopy
def calculate_distance(lat1, lon1, lat2, lon2):
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    return geodesic(loc1, loc2).kilometers

# Prediction function
def predict_prices(chosen_commodity, chosen_variety, chosen_district, quantity, chosen_month, chosen_year):
    try:
        current_lat, current_lon = get_lat_lon_from_district(chosen_district)
    except ValueError as e:
        return {"error": str(e)}

    # Prepare input data (considering the variety input now)
    input_data = [[chosen_commodity, chosen_variety, chosen_district, chosen_year, chosen_month]]

    predicted_price = rf_model.predict(input_data)[0]
    total_cost = (predicted_price / 100) * quantity

    # Example of dummy nearby districts for simplicity
    nearby_districts_info = [
        {"District": "Nearby District 1", "distance": 20.5, "Modal_Price": 1500},
        {"District": "Nearby District 2", "distance": 40.3, "Modal_Price": 1450},
        {"District": "Nearby District 3", "distance": 50.1, "Modal_Price": 1600},
    ]

    return {
        "predictedPrice": predicted_price,
        "totalCost": total_cost,
        "nearbyDistricts": nearby_districts_info,
        # Uncomment and replace with actual logic if you have a method to determine best buy month
        # "bestBuyMonth": "January"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Use get_json() to handle JSON input
    district = data['district']
    commodity = data['commodity']
    variety = data['variety']  # Retrieve the variety
    amount = float(data['amount'])
    month = int(data['month'])
    year = int(data['year'])

    # Call the prediction logic
    result = predict_prices(commodity, variety, district, amount, month, year)

    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    # If you have logic to determine the best buy month, uncomment and replace the following line
    # result["bestBuyMonth"] = "January"

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
