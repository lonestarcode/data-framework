import numpy as np
import pandas as pd
from typing import Dict, Any, List

class PropertyAnalyzer:
    def __init__(self):
        self.risk_factors = {
            'market_volatility': 0.15,
            'property_condition': 0.25,
            'location_score': 0.3,
            'economic_indicators': 0.3
        }
    
    def calculate_market_feasibility(
        self,
        property_data: Dict[str, Any],
        market_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates market feasibility score and risk assessment
        """
        try:
            # Calculate various scores
            location_score = self._calculate_location_score(property_data)
            market_score = self._analyze_market_conditions(market_conditions)
            risk_score = self._assess_risk_factors(property_data, market_conditions)
            
            # Calculate overall feasibility
            feasibility_score = (
                location_score * 0.4 +
                market_score * 0.35 +
                (1 - risk_score) * 0.25
            )
            
            return {
                'feasibility_score': feasibility_score,
                'location_score': location_score,
                'market_score': market_score,
                'risk_score': risk_score,
                'recommendations': self._generate_recommendations(feasibility_score, property_data)
            }
            
        except Exception as e:
            logging.error(f"Error in feasibility calculation: {str(e)}")
            raise

    def estimate_financial_projections(
        self,
        property_value: float,
        down_payment: float,
        loan_amount: float,
        interest_rate: float,
        loan_term: int,
        property_data: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates comprehensive financial projections including both costs and revenue
        """
        try:
            # Get fixed costs
            fixed_costs = self.estimate_fixed_costs(property_value, property_data)
            
            # Get revenue estimates
            revenue = self.estimate_revenue(property_data, market_data)
            
            # Calculate mortgage details
            mortgage = self._calculate_mortgage_payment(loan_amount, interest_rate, loan_term)
            
            # Calculate net operating income
            noi = {
                'conservative': revenue['revenue_scenarios']['conservative']['annual'] - fixed_costs['total_annual'],
                'expected': revenue['revenue_scenarios']['expected']['annual'] - fixed_costs['total_annual'],
                'optimistic': revenue['revenue_scenarios']['optimistic']['annual'] - fixed_costs['total_annual']
            }
            
            # Calculate cash flow
            cash_flow = {
                scenario: {
                    'monthly': (noi[scenario] - mortgage['annual_payment']) / 12,
                    'annual': noi[scenario] - mortgage['annual_payment']
                }
                for scenario in ['conservative', 'expected', 'optimistic']
            }
            
            return {
                'revenue': revenue,
                'fixed_costs': fixed_costs,
                'mortgage': mortgage,
                'noi': noi,
                'cash_flow': cash_flow,
                'cap_rate': {
                    scenario: (noi[scenario] / property_value) * 100
                    for scenario in ['conservative', 'expected', 'optimistic']
                }
            }
            
        except Exception as e:
            logging.error(f"Error in financial projections: {str(e)}")
            raise

    def _generate_recommendations(self, feasibility_score: float, property_data: Dict[str, Any]) -> List[str]:
        recommendations = []
        
        # Overall feasibility recommendation
        if feasibility_score >= 0.8:
            recommendations.append("Strong investment opportunity - Consider aggressive investment")
        elif feasibility_score >= 0.6:
            recommendations.append("Moderate opportunity - Proceed with standard due diligence")
        else:
            recommendations.append("Higher risk investment - Additional research recommended")
        
        # Location-based recommendation
        if self.location_score >= 0.75:
            recommendations.append("Prime location with strong appreciation potential")
        elif self.location_score <= 0.4:
            recommendations.append("Location may limit future appreciation potential")
        
        # Market-based recommendation
        if self.market_score >= 0.7:
            recommendations.append("Current market conditions are favorable for investment")
        elif self.market_score <= 0.4:
            recommendations.append("Consider waiting for more favorable market conditions")
        
        # Risk-based recommendation
        if self.risk_score <= 0.3:
            recommendations.append("Low risk profile - Suitable for conservative investors")
        elif self.risk_score >= 0.7:
            recommendations.append("High risk profile - Consider risk mitigation strategies")
        
        return recommendations

    # Additional helper methods...