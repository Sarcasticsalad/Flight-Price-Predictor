import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
from pydantic import BaseModel
import pickle
import os
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from typing import List
import json
from starlette.requests import Request

# App object
app = FastAPI()

# Enable CORS
origins = ["http://localhost:5173"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlightData(BaseModel):
    departure_date: str
    departure: str
    arrival_date: str
    destination: str
    airline: str
    flight_class: str
    stops: int
    travel_time: int

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the pickle file
pickle_file_path = os.path.join(current_dir, "..", "backend_ml", "machine_learning", "flight_price_rf_v2.pkl")

# Load Machine Learning Model
pickle_in = open(pickle_file_path, "rb")
rf_reg_model = pickle.load(pickle_in)

# List of airlines
Airline_names = [
    'Air Arabia', 'Air Canada', 'Air China', 'Air France', 'Air India',
    'American Airlines', 'Austrian', 'British Airways', 'Brusseis',
    'Cathay Pacific', 'China Eastern', 'China Southern', 'Delta',
    'Easy Jet', 'Emirates', 'Etihad', 'IndiGo', 'Korean Air',
    'Lufthansa', 'Luxiar', 'Malaysia Airlines', 'Malindo Air',
    'Nepal Airlines', 'Qantas', 'Qatar Airways', 'SWISS',
    'Singapore Airlines', 'SriLankan Airlines', 'THAI',
    'Turkish Airlines', 'United Airlines', 'Virgin Atlantic',
    'Vueling', 'flydubai']

# List of departure locations
Departure_locations = ['Beijing', 'Berlin', 'Chicago',
                       'Delhi', 'Dubai', 'Kathmandu', 'London', 'New Delhi', 'New York',
                       'Paris', 'Sydney']

# List of destination locations
Destination_locations = ['Beijing', 'Berlin', 'Chicago', 'Dubai',
                          'Kathmandu', 'London', 'New Delhi',
                          'New York', 'Singapore', 'Sydney']

# List of weekdays

weekdays = ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']

# List of flight class types
Flight_Class_type = ['Business', 'Economy', 'First']

# Function to preprocess the input
def preprocess_data(Airline, Departure, Destination, Departure_date, Arrival_date, Stops, Travel_time, Flight_Class):
    # Define the weekdays list
    weekdays = ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']

    # Extracting month and date from departure and arrival dates
    departure_month = pd.to_datetime(Departure_date).month
    departure_day = pd.to_datetime(Departure_date).day
    arrival_month = pd.to_datetime(Arrival_date).month
    arrival_day = pd.to_datetime(Arrival_date).day

    # Convert date of the day to week day and one-hot encode it
    departure_weekday = pd.to_datetime(Departure_date).strftime('%A')
    departure_weekday_encoded = [int(departure_weekday == day) for day in weekdays]

    # Encoding code 2.0
    Airline_encoded = [int(Airline == name) for name in Airline_names]
    Departure_encoded = [int(Departure == loc) for loc in Departure_locations]
    Destination_encoded = [int(Destination == loc) for loc in Destination_locations]
    Flight_Class_encoded = [int(Flight_Class == fc_type) for fc_type in Flight_Class_type]

    # Combine all features into a single array
    features = np.array([
        Stops, Travel_time, departure_month, departure_day, arrival_month, arrival_day
    ] + Airline_encoded + Departure_encoded + Destination_encoded
      + departure_weekday_encoded + Flight_Class_encoded)

    # Reshape the array to have a shape (1, number_of_features)
    features = features.reshape(1, -1)

    return features
 

# Routes
@app.get("/")
async def root():
    return {"request": "Hello world"}


@app.post("/predict")
async def read_predict_data(data: dict):
    try:
        # Print received data
        # print(data["data"]["airline"])
        data = data["data"]
        # print(data)
        features = preprocess_data(
        data["airline"], data["departure"], data["destination"],
        data["departure_date"], data["arrival_date"],
        int(data["stops"]), int(data["travel_time"]), data["flight_class"]
        )


        # Create a DataFrame with feature names
        feature_names = ['Stops', 'Travel_Time', 'Departure_Month', 'Departure_Day',
       'Arrival_Month', 'Arrival_Day', 'Airline_Air Arabia',
       'Airline_Air Canada', 'Airline_Air China', 'Airline_Air France',
       'Airline_Air India', 'Airline_American Airlines', 'Airline_Austrian',
       'Airline_British Airways', 'Airline_Brusseis', 'Airline_Cathay Pacific',
       'Airline_China Eastern', 'Airline_China Southern', 'Airline_Delta',
       'Airline_Easy Jet', 'Airline_Emirates', 'Airline_Etihad',
       'Airline_IndiGo', 'Airline_Korean Air', 'Airline_Lufthansa',
       'Airline_Luxiar', 'Airline_Malaysia Airlines', 'Airline_Malindo Air',
       'Airline_Nepal Airlines', 'Airline_Qantas', 'Airline_Qatar Airways',
       'Airline_SWISS', 'Airline_Singapore Airlines',
       'Airline_SriLankan Airlines', 'Airline_THAI',
       'Airline_Turkish Airlines', 'Airline_United Airlines',
       'Airline_Virgin Atlantic', 'Airline_Vueling', 'Airline_flydubai',
       'Departure_Beijing', 'Departure_Berlin', 'Departure_Chicago',
       'Departure_Delhi', 'Departure_Dubai', 'Departure_Kathmandu',
       'Departure_London', 'Departure_New Delhi', 'Departure_New York',
       'Departure_Paris', 'Departure_Sydney', 'Destination_Beijing',
       'Destination_Berlin', 'Destination_Chicago', 'Destination_Dubai',
       'Destination_Kathmandu', 'Destination_London', 'Destination_New Delhi',
       'Destination_New York', 'Destination_Singapore', 'Destination_Sydney',
       'Day_of_the_week_Friday', 'Day_of_the_week_Monday',
       'Day_of_the_week_Saturday', 'Day_of_the_week_Sunday',
       'Day_of_the_week_Thursday', 'Day_of_the_week_Tuesday',
       'Day_of_the_week_Wednesday', 'Flight_Class_Business',
       'Flight_Class_Economy', 'Flight_Class_First']
        

        features_df = pd.DataFrame(features, columns=feature_names)

        print(features_df)

        # Predicting
        predict_price = rf_reg_model.predict(features_df)
        # predict_price = round(predict_price,2)    
        predict_price = str(round(predict_price[0] * 130,2))
        
        print(predict_price)

        return JSONResponse({"price":predict_price})

    except Exception as e:
        print("Error processing request:", e)
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

    