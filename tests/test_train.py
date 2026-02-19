import subprocess
from pathlib import Path
import joblib
import pandas as pd
import yaml

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

def test_train():
    # Run the train script
    result = subprocess.run(["python", "-m", "src.stages.train"], 
                            capture_output=True, 
                            text=True)
    
    # Check if the script ran successfully
    assert result.returncode == 0, f"Train script failed with error: {result.stderr}"
    
    # Check if the model file was created
    model_file = Path(params['model']['path'])
    assert model_file.exists(), "Model file was not created."

    model = joblib.load(model_file)
    assert model is not None, "Model could not be loaded from file."    