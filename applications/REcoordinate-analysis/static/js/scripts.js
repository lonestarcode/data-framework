let scenarios = [];

function collectFormData() {
    return {
        street: document.getElementById('street').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        latitude: document.getElementById('latitude').value,
        longitude: document.getElementById('longitude').value,
        down_payment: parseFloat(document.getElementById('downPayment').value),
        loan_amount: parseFloat(document.getElementById('loanAmount').value),
        interest_rate: parseFloat(document.getElementById('interestRate').value),
        loan_term: parseInt(document.getElementById('loanTerm').value),
        analysis_years: parseInt(document.getElementById('analysisYears').value) || 5,
        appreciation_rate: parseFloat(document.getElementById('appreciationRate').value) || 3,
        pets_allowed: document.getElementById('petsAllowed').value === 'true',
        parking_spots: parseInt(document.getElementById('parkingSpots').value) || 0,
        storage_units: parseInt(document.getElementById('storageUnits').value) || 0,
        utility_markup: parseFloat(document.getElementById('utilityMarkup').value) || 0,
        base_rent: parseFloat(document.getElementById('baseRent').value) || 0,
        occupancy_rate: parseFloat(document.getElementById('occupancyRate').value) || 95
    };
}

function clearInputs() {
    document.getElementById('street').value = '';
    document.getElementById('city').value = '';
    document.getElementById('state').value = '';
    document.getElementById('latitude').value = '';
    document.getElementById('longitude').value = '';
    document.getElementById('downPayment').value = '';
    document.getElementById('loanAmount').value = '';
    document.getElementById('interestRate').value = '';
    document.getElementById('loanTerm').value = '30';
    document.getElementById('analysisYears').value = '5';
    document.getElementById('appreciationRate').value = '3';
    document.getElementById('rentalIncome').value = '';
}

function updateLocation() {
    const data = collectFormData();
    
    fetch('/api/property-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        scenarios.push(data);
        
        // Ask user if they want to add another scenario
        if (confirm("Do you want to input another scenario to compare?")) {
            clearInputs();
        } else {
            displayAdvancedAnalysis(scenarios);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error analyzing property. Please try again.');
    });
}

function runAdvancedAnalysis() {
    const data = collectFormData();
    
    fetch('/api/property-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        scenarios.push(data);
        displayAdvancedAnalysis(scenarios);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error running analysis. Please try again.');
    });
}

function displayAdvancedAnalysis(scenarios) {
    const resultsContainer = document.getElementById('advancedAnalysisResults');
    resultsContainer.innerHTML = '';

    scenarios.forEach((scenario, index) => {
        const scenarioDiv = document.createElement('div');
        scenarioDiv.classList.add('analysis-section');
        
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            maximumFractionDigits: 0
        });

        scenarioDiv.innerHTML = `
            <h4>Scenario ${index + 1} Analysis</h4>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <span class="metric-label">Property Value:</span>
                    <span class="metric-value">${formatter.format(scenario.property_data.value)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Monthly Payment:</span>
                    <span class="metric-value">${formatter.format(scenario.projections.mortgage.monthly_payment)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Monthly Revenue:</span>
                    <span class="metric-value">${formatter.format(scenario.projections.revenue.expected.monthly)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Net Operating Income:</span>
                    <span class="metric-value">${formatter.format(scenario.projections.noi.expected)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Cash Flow:</span>
                    <span class="metric-value">${formatter.format(scenario.projections.cash_flow.expected.monthly)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Cap Rate:</span>
                    <span class="metric-value">${scenario.projections.cap_rate.expected.toFixed(2)}%</span>
                </div>
            </div>

            <h5>Revenue Breakdown</h5>
            <div class="metrics-grid">
                <div class="metric-item">
                    <span class="metric-label">Base Rental Income:</span>
                    <span class="metric-value">${formatter.format(scenario.projections.revenue.base_monthly_rent)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Additional Revenue:</span>
                    <span class="metric-value">${formatter.format(
                        Object.values(scenario.projections.revenue.additional_revenue).reduce((a, b) => a + b, 0)
                    )}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Occupancy Rate:</span>
                    <span class="metric-value">${scenario.projections.revenue.occupancy_metrics.average_occupancy_rate * 100}%</span>
                </div>
            </div>

            <h5>AI Investment Analysis</h5>
            <div class="metrics-grid">
                <div class="metric-item">
                    <span class="metric-label">Market Score:</span>
                    <span class="metric-value">${(scenario.feasibility.market_score * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Location Score:</span>
                    <span class="metric-value">${(scenario.feasibility.location_score * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Risk Score:</span>
                    <span class="metric-value">${(scenario.feasibility.risk_score * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Overall Feasibility:</span>
                    <span class="metric-value">${(scenario.feasibility.feasibility_score * 100).toFixed(1)}%</span>
                </div>
            </div>

            <h5>Future Value Prediction</h5>
            <div class="metrics-grid">
                <div class="metric-item">
                    <span class="metric-label">5 Year Estimate:</span>
                    <span class="metric-value">${formatter.format(scenario.future_value.five_year)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">10 Year Estimate:</span>
                    <span class="metric-value">${formatter.format(scenario.future_value.ten_year)}</span>
                </div>
            </div>

            <div class="recommendations">
                <h5>AI Recommendations</h5>
                <ul>
                    ${scenario.feasibility.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;

        resultsContainer.appendChild(scenarioDiv);
    });
}

function exportToExcel() {
    if (scenarios.length === 0) {
        alert('Please run at least one analysis before exporting.');
        return;
    }

    fetch('/api/export-excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(scenarios)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `property_analysis_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error exporting to Excel. Please try again.');
    });
}

function searchByAddress() {
    const street = document.getElementById('street').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;

    const data = { street, city, state };

    fetch('/api/property-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle the response data
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error searching by address. Please try again.');
    });
}

function searchByCoordinates() {
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;

    const data = { latitude, longitude };

    fetch('/api/property-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle the response data
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error searching by coordinates. Please try again.');
    });
} 