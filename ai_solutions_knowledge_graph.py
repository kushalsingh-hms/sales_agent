"""
AI Solutions Knowledge Graph
This module contains a structured knowledge graph of AI solutions across different sectors.
Each solution includes problem statements, AI techniques, business impacts, and cross-sector connections.
"""

AI_SOLUTIONS_GRAPH = {
    "healthcare": {
        "patient_care_optimization": {
            "problem": "Inefficient patient scheduling and resource allocation",
            "solution": "Predictive analytics + ML scheduling",
            "impact": {
                "wait_times": "30% reduction",
                "resource_utilization": "20% improvement"
            },
            "data_sources": [
                "Patient history",
                "Appointment patterns",
                "Resource availability"
            ],
            "quick_pitch": "Our AI can predict patient no-shows and optimize your schedule, reducing wait times by 30%",
            "cross_sector": {
                "similar_to": "retail_inventory_optimization",
                "connection": "Resource optimization and scheduling"
            }
        },
        "medical_imaging_analysis": {
            "problem": "Time-consuming image analysis and diagnosis",
            "solution": "Computer vision + Deep learning",
            "impact": {
                "diagnosis_speed": "40% faster",
                "detection_accuracy": "25% improvement"
            },
            "data_sources": [
                "X-rays",
                "MRIs",
                "CT scans"
            ],
            "quick_pitch": "Our AI can analyze medical images 40% faster while improving accuracy by 25%",
            "cross_sector": {
                "similar_to": "manufacturing_quality_control",
                "connection": "Image-based quality assessment"
            }
        }
    },
    "finance": {
        "fraud_detection": {
            "problem": "Increasing financial fraud and security threats",
            "solution": "Anomaly detection + Pattern recognition",
            "impact": {
                "detection_speed": "60% faster",
                "loss_reduction": "35% reduction"
            },
            "data_sources": [
                "Transaction history",
                "User behavior patterns"
            ],
            "quick_pitch": "Our AI detects fraudulent transactions in real-time, reducing losses by 35%",
            "cross_sector": {
                "similar_to": "healthcare_insurance_fraud",
                "connection": "Pattern-based fraud detection"
            }
        },
        "credit_risk_assessment": {
            "problem": "Inaccurate credit scoring and risk evaluation",
            "solution": "Predictive analytics + ML models",
            "impact": {
                "risk_prediction": "25% more accurate",
                "loan_approval": "15% better rates"
            },
            "data_sources": [
                "Credit history",
                "Financial behavior",
                "Market trends"
            ],
            "quick_pitch": "Our AI improves credit risk assessment accuracy by 25%, helping you make better lending decisions",
            "cross_sector": {
                "similar_to": "student_performance_prediction",
                "connection": "Predictive analytics for risk assessment"
            }
        }
    },
    "retail": {
        "personalized_recommendations": {
            "problem": "Low customer engagement and conversion rates",
            "solution": "Recommendation systems + NLP",
            "impact": {
                "sales_increase": "30% increase",
                "customer_satisfaction": "40% higher"
            },
            "data_sources": [
                "Purchase history",
                "Browsing behavior",
                "Customer preferences"
            ],
            "quick_pitch": "Our AI personalizes shopping experiences, increasing sales by 30%",
            "cross_sector": {
                "similar_to": "education_personalized_learning",
                "connection": "Personalized content delivery"
            }
        },
        "inventory_optimization": {
            "problem": "Stockouts and overstocking issues",
            "solution": "Predictive analytics + Demand forecasting",
            "impact": {
                "stockout_reduction": "25% reduction",
                "inventory_costs": "20% lower"
            },
            "data_sources": [
                "Sales history",
                "Seasonal trends",
                "Market conditions"
            ],
            "quick_pitch": "Our AI predicts demand patterns, reducing stockouts by 25% while cutting inventory costs",
            "cross_sector": {
                "similar_to": "healthcare_patient_scheduling",
                "connection": "Resource optimization"
            }
        }
    },
    "manufacturing": {
        "predictive_maintenance": {
            "problem": "Unexpected equipment failures and downtime",
            "solution": "IoT + Predictive analytics",
            "impact": {
                "downtime_reduction": "40% reduction",
                "maintenance_costs": "30% lower"
            },
            "data_sources": [
                "Sensor data",
                "Equipment performance",
                "Maintenance history"
            ],
            "quick_pitch": "Our AI predicts equipment failures before they happen, reducing downtime by 40%",
            "cross_sector": {
                "similar_to": "healthcare_equipment_maintenance",
                "connection": "Predictive maintenance"
            }
        },
        "quality_control": {
            "problem": "Defective products and quality issues",
            "solution": "Computer vision + ML classification",
            "impact": {
                "inspection_speed": "50% faster",
                "defect_reduction": "35% reduction"
            },
            "data_sources": [
                "Product images",
                "Quality metrics",
                "Production parameters"
            ],
            "quick_pitch": "Our AI inspects products 50% faster while reducing defects by 35%",
            "cross_sector": {
                "similar_to": "healthcare_medical_imaging",
                "connection": "Image-based quality assessment"
            }
        }
    },
    "education": {
        "personalized_learning": {
            "problem": "One-size-fits-all education approach",
            "solution": "Adaptive learning + NLP",
            "impact": {
                "learning_outcomes": "30% better",
                "student_engagement": "40% higher"
            },
            "data_sources": [
                "Student performance",
                "Learning patterns",
                "Content interaction"
            ],
            "quick_pitch": "Our AI creates personalized learning paths, improving outcomes by 30%",
            "cross_sector": {
                "similar_to": "retail_personalized_recommendations",
                "connection": "Personalized content delivery"
            }
        },
        "student_performance_prediction": {
            "problem": "Difficulty identifying at-risk students",
            "solution": "Predictive analytics + ML models",
            "impact": {
                "intervention_timing": "35% earlier",
                "retention_rates": "25% better"
            },
            "data_sources": [
                "Grades",
                "Attendance",
                "Engagement metrics"
            ],
            "quick_pitch": "Our AI identifies at-risk students early, improving retention by 25%",
            "cross_sector": {
                "similar_to": "finance_credit_risk",
                "connection": "Predictive analytics for risk assessment"
            }
        }
    }
}

def get_solution_by_sector(sector):
    """Get all solutions for a specific sector."""
    return AI_SOLUTIONS_GRAPH.get(sector.lower(), {})

def get_solution_details(sector, solution_name):
    """Get detailed information about a specific solution."""
    sector_solutions = get_solution_by_sector(sector)
    return sector_solutions.get(solution_name.lower(), {})

def find_cross_sector_solutions(problem_keywords):
    """Find solutions across sectors that match given problem keywords."""
    matching_solutions = []
    for sector, solutions in AI_SOLUTIONS_GRAPH.items():
        for solution_name, details in solutions.items():
            if any(keyword.lower() in details["problem"].lower() for keyword in problem_keywords):
                matching_solutions.append({
                    "sector": sector,
                    "solution": solution_name,
                    "details": details
                })
    return matching_solutions

def get_quick_pitch(sector, solution_name):
    """Get the quick pitch for a specific solution."""
    solution = get_solution_details(sector, solution_name)
    return solution.get("quick_pitch", "") 