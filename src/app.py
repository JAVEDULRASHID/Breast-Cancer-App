import joblib
import yaml
from src.logger import get_logger
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

logger = get_logger(__name__, component="main application")


def create_app():
    main_app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    main_app.secret_key = 'your_secret_key'
    logger.info("Creating main application...")
    logger.info("Loading model and features...")
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)

  
    model = joblib.load(params['model']['trained_model'])
    #model = joblib.load(params['model']['path'])
    FEATURES = model.feature_names_in_

    @main_app.route('/', methods=['GET'])
    def index():
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error in index route: {e}")
            return render_template('error.html', error=str(e))
        

    @main_app.route('/form', methods=['POST'])
    def predict():
        try:
            input_data = [float(request.form.get(f)) for f in FEATURES]
            df = pd.DataFrame([input_data], columns=FEATURES)
            # Make prediction
            prediction = model.predict(df)
            if prediction[0] == 1:
                prediction = 'Malignant'
                
            else:                    
                prediction = 'Benign'
            # Return prediction result
            return render_template('result.html', prediction=prediction)
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return render_template('error.html', error=str(e))
    logger.info("Main application created successfully.")
    return main_app

if __name__ == "__main__":   
    main_app = create_app()
    logger.info("Starting the main application...")
    main_app.run(host='0.0.0.0', port=3030, debug=True,)