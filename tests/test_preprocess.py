import subprocess
from pathlib import Path
import pandas as pd
import yaml

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)


def test_preprocess():
    # Run the preprocess script
    result = subprocess.run(["python", "-m", "src.stages.dataset"], 
                            capture_output=True, 
                            text=True)
    
    # Check if the script ran successfully
    assert result.returncode == 0, f"Preprocess script failed with error: {result.stderr}"
    
    # Check if the processed data file was created
    processed_file = Path(params['data']['processed'])
    assert processed_file.exists(), "Processed data file was not created."
    
    # Optionally, check the contents of the processed data
    df = pd.read_csv(processed_file)
    assert not df.empty, "Processed data file is empty."