import yaml
from src.logger import get_logger
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
from src.stages.model import get_model
import joblib
import os
logger = get_logger(__name__, component="train model")


with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

def train_model():
    try:
        df = pd.read_csv(params['data']['processed'])  # Get the processed data and selected features
        
        train, test = train_test_split(df, test_size=0.2, random_state=42)  # Split the data into training and testing sets
        
        train_x = train.drop(columns=['diagnosis'])  # Features for training
        train_y = train['diagnosis']  # Target variable for training

        test_x = test.drop(columns=['diagnosis'])  # Features for testing
        test_y = test['diagnosis']  # Target variable for testing



        logger.info("Data split into training and testing sets successfully")

        model = get_model(params['model']['name'])  # Get the model based on the name specified in params.yaml
        model.fit(train_x, train_y)  # Train the model on the training data

        model.predict(test_x)  # Make predictions on the testing data to ensure the model is working

        #saving the model to a file
        os.makedirs(os.path.dirname(params['model']['path']), exist_ok=True)
        joblib.dump(model, params['model']['path'])  # Save the trained model to a file
        logger.info(f"Model trained and saved to {params['model']['path']} successfully")

        return model,train_x,train_y,test_x,test_y

    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise e
def evaluate_model(test_y):
    try:
        logger.info("Starting model evaluation")
        # model evaluation code here
        loaded_model = joblib.load(params['model']['path'])
        predictions = loaded_model.predict(test_x)
        accuracy = accuracy_score(test_y, predictions)
        
        logger.info("Model evaluation completed successfully with accuracy: {:.2f}%".format(accuracy * 100))
        return accuracy
    
    except Exception as e:
        logger.error(f"Error during model evaluation: {e}")
        raise e
if __name__ == "__main__":
    model,train_x,train_y,test_x,test_y = train_model()
    score = evaluate_model(test_y=test_y)
    