from sqlalchemy import create_engine
import pandas as pd


class LoadCsv:

    def __init__(self):

        self.engine = create_engine('postgresql://postgres:epona27@localhost:5432/dev_keet')

    def load_pandas(self, file):
        df = pd.read_csv(file)
        df.to_sql('users', self.engine)


