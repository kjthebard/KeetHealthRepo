import pandas as pd
from sqlalchemy import create_engine

class TransformData:

    def __init__(self):

        self.engine = create_engine('postgresql://postgres:epona27@localhost:5432/dev_keet')

    def transform_data(self):

        """
        load to pandas takes in nothing and returns the data as promised.
        :return: Nothing, database gets a table called "daily_user_counts"
        """

        # connect to and read from the data
        conn = self.engine.connect()

        # would not recommend in a big data environment, obv select only what you need! For this example making it simple
        df = pd.read_sql("select * from users", conn)

        # get a count by user id grouping by visit_date
        count = df[['id', 'visit_date']].groupby('visit_date').count()

        # Need to reset the index after the groupby as date is in index
        count.reset_index(inplace=True)

        # Convert object type after dataframe index reset into datetime so I can do the next part easily
        count['visit_date'] = pd.to_datetime(count['visit_date'])

        # Wow... very simple, love pandas, spark has identical functionality
        count['year'] = count['visit_date'].dt.year
        count['month'] = count['visit_date'].dt.month
        count['day'] = count['visit_date'].dt.day

        # rename id column into what it should be called: count
        renamed_count = count.rename(columns={"id":"count"})

        # Can'r predict based on 1 day, so first day will be empty
        prediction = renamed_count["count"].rolling(2).mean()

        # append the prediction to the dataframe
        renamed_count["observed"] = prediction

        # reorganize so that the table has the columns in the order stated in the code challenge
        final_df = renamed_count[['year', 'month', 'day', 'observed', 'count']]

        # write the table out
        final_df.to_sql('daily_user_counts', self.engine)
