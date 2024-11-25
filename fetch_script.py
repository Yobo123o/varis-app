import os
import sqlite3
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

# API Endpoint and Database Configuration
API_URL = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json"
DATABASE = "api_data.db"


# Fetch data from API
def fetch_api_data(limit=10):
    headers = {
        "X-Api-Key": API_KEY
    }
    params = {
        "limit": limit
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["fuel_stations"]  # Adjust based on the API structure
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


# Save data to SQLite
def save_to_database(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fuel_stations (
        id INTEGER PRIMARY KEY,
        station_name TEXT,
        street_address TEXT,
        city TEXT,
        state TEXT,
        zip TEXT
    )
    """)

    # Insert data
    for item in data:
        cursor.execute("""
        INSERT INTO fuel_stations (id, station_name, street_address, city, state, zip)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["id"],
            item["station_name"],
            item["street_address"],
            item["city"],
            item["state"],
            item["zip"]
        ))

    conn.commit()
    conn.close()


# Main Workflow
data = fetch_api_data(limit=10)
if data:
    save_to_database(data)
    print("Data saved to database.")
