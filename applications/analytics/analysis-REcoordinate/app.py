from flask import Flask, request, jsonify, render_template, send_file
from flask_wtf.csrf import CSRFProtect
import pandas as pd
import io
from datetime import datetime
from utils.data_fetching import fetch_property_data, get_property_details
from utils.analysis import (
    calculate_market_feasibility,
    estimate_financial_projections,
    calculate_growth_potential
)
from utils.ml_models import predict_future_value
import logging
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config.update(
    GOOGLE_MAPS_API_KEY=os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY'),
    SECRET_KEY=os.getenv('SECRET_KEY', 'your-secret-key-here')
)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def geocode_address(street, city, state):
    """Geocode an address using Google Maps API"""
    api_key = app.config['GOOGLE_MAPS_API_KEY']
    address = f"{street}, {city}, {state}"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('results')
            if results:
                location = results[0]['geometry']['location']
                return location['lat'], location['lng']
    except Exception as e:
        logging.error(f"Geocoding error: {str(e)}")
    
    return None, None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html',
        google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY']
    )

@app.route('/api/property-analysis', methods=['POST'])
def analyze_property():
    """Analyze property based on provided data"""
    try:
        data = request.json
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Determine which input to use
        if not latitude or not longitude:
            if street and city and state:
                latitude, longitude = geocode_address(street, city, state)
                if latitude is None or longitude is None:
                    return jsonify({'error': 'Invalid address provided'}), 400
            else:
                return jsonify({'error': 'Insufficient data provided'}), 400
        
        # Log the coordinates
        logging.info(f"Processing property at coordinates: {latitude}, {longitude}")
        
        # Fetch property data
        property_data = fetch_property_data(latitude, longitude)
        
        # Get detailed property information
        details = get_property_details(property_data['address'])
        
        # Use default values if not provided
        analysis_years = data.get('analysis_years', 5)
        appreciation_rate = data.get('appreciation_rate', 3)
        
        # Calculate market feasibility
        feasibility = calculate_market_feasibility(
            property_data,
            market_conditions=data.get('market_conditions', {})
        )
        
        # Calculate financial projections
        projections = estimate_financial_projections(
            property_value=property_data['value'],
            down_payment=data.get('down_payment', 0),
            loan_amount=data.get('loan_amount', 0),
            interest_rate=data.get('interest_rate', 0),
            loan_term=data.get('loan_term', 30),
            rental_income=data.get('rental_income', 0),
            analysis_years=analysis_years,
            appreciation_rate=appreciation_rate
        )
        
        # Predict future value using ML model
        future_value = predict_future_value(property_data)
        
        response = {
            'property_data': property_data,
            'details': details,
            'feasibility': feasibility,
            'projections': projections,
            'future_value': future_value
        }
        
        return jsonify(response)
    
    except Exception as e:
        logging.error(f"Error in property analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-excel', methods=['POST'])
def export_excel():
    """Export analysis results to Excel"""
    try:
        data = request.json
        
        # Create Excel file in memory
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        # Create different sheets for different aspects of the analysis
        sheets = {
            'Property Details': pd.DataFrame([data['property_data']]),
            'Financial Projections': pd.DataFrame(data['projections']),
            'Market Analysis': pd.DataFrame([data['feasibility']]),
            'Future Value Predictions': pd.DataFrame([data['future_value']])
        }
        
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        writer.save()
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'property_analysis_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
    
    except Exception as e:
        logging.error(f"Error in Excel export: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure the logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    app.run(debug=True)