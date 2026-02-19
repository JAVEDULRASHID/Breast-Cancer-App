from src.logger import get_logger
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

logger = get_logger(__name__, component="model class")

def get_model(model_name):
    try:
        if model_name == "knn":
            model = KNeighborsClassifier()
        elif model_name == "random_forest":
            model = RandomForestClassifier()
        elif model_name == "logistic_regression":
            model = LogisticRegression()
        else:
            raise ValueError(f"Unsupported model name: {model_name}")
        
        logger.info(f"{model_name} model created successfully")
        return model
    
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise e 



