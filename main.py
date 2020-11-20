from solution.load_csv import LoadCsv
from solution.transform_data import TransformData

import os

# Initialize Classes
L = LoadCsv()
T = TransformData()

# Call Functions
L.load_pandas(file=os.path.dirname(__file__)+"/data/users.csv")
T.transform_data()


