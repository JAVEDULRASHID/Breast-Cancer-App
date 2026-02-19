from pathlib import Path
import yaml
from src.app import create_app

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

def test_api():
    # Create a test client for the Flask app
    app = create_app()
    with app.test_client() as client:
        # Test the index route
        response = client.get('/')
        assert response.status_code == 200, "Index route did not return 200 OK"
        
        # Test the form submission route with valid data
        test_data = {
            'perimeter_se': '0.1',
            'area_worst': '0.2',
            'concavity_worst': '0.3',
            'radius_se': '0.4',
            'compactness_worst': '0.5',
            'area_se': '0.6',
            'concavity_mean': '0.7',
            'concave points_mean': '0.8',
            'radius_mean': '0.9',
            'perimeter_mean': '1.0',
            'compactness_mean': '1.1',
            'concave points_worst': '1.2',
            'area_mean': '1.3',
            'radius_worst': '1.4',
            'perimeter_worst': '1.5'
        }
        response = client.post('/form', data=test_data)
        assert response.status_code == 200, "Form submission did not return 200 OK"
        
        assert b'Malignant' in response.data or b'Benign' in response.data, "Prediction result not found in response"