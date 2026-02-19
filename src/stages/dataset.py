from src.logger import get_logger
import yaml
import pandas as pd
import os


logger = get_logger(__name__, component="data processing")

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

def get_data():
    try:
        logger.info("Starting data ingestion")  
        df = pd.read_csv(params['data']['source'])    
        logger.info("Data loaded from csv file successfully")  
        
        df = df.drop(columns=['id','Unnamed: 32'])  # Drop the 'id' and 'Unnamed: 32' column if it exists
        df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})  # Map 'M' to 1 and 'B' to 0
        
        mean_list = list(df.columns[1:11])  
        se_list = list(df.columns[11:21])  
        worst_list = list(df.columns[21:31])
        
        mean_list.append('diagnosis')
        se_list.append('diagnosis')
        worst_list.append('diagnosis')
        
        corr_mean = df[mean_list].corr()  
        corr_se = df[se_list].corr()  
        corr_worst = df[worst_list].corr()  

        mean_features = list(corr_mean[corr_mean['diagnosis']>0.5].index)
        se_features = list(corr_se[corr_se['diagnosis']>0.5].index)
        worst_features = list(corr_worst[corr_worst['diagnosis']>0.5].index)

        pred_var= mean_features + se_features + worst_features
        pred_var = list(set(pred_var))  

        processed_data = df[pred_var]
        processed_data_path = params['data']['processed']
        os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
        processed_data.to_csv(processed_data_path, index=False)
        
        logger.info("Data processing completed and saved to csv file successfully")

        return processed_data
    
    except Exception as e:
        logger.error(f"Error during data processing: {e}")
        raise e 
    
    
if __name__ == "__main__":
    get_data()