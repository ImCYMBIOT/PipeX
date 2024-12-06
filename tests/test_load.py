import pytest
import pandas as pd
from app.load import load_data

def test_load_data_to_csv(mocker):
    mocker.patch("pandas.DataFrame.to_csv")
    
    data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    load_data(
        target="file",
        config={'file_type': 'csv', 'file_path': 'path/to/your/file.csv'},
        data=data
    )
    
    pd.DataFrame.to_csv.assert_called_once_with('path/to/your/file.csv', index=False)