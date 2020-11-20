import psycopg2
from improvements.sql_template import users
import yaml
import os
from glob import glob

class Load:

    def __init__(self):

        self.templates = glob(os.path.dirname(__file__)[:-5] + "/templates/*.yml") ## This is a hack to make paths work on any system. IRL wouldn't do this.
        self.data = glob(os.path.dirname(__file__)[:-5] + "/data/users.csv") ## Again trying I'm working on my home PC, need it to work locally on all computers.
        self.configs = []
        self.sql_scripts = []

    def load_configs(self):
        # Loading configs from yml files... This way I can render all of my sql statements across my environments at once.

        for file in self.templates:
            with open(file, 'r') as f:
                self.configs.append(yaml.safe_load(f))

        self.create_pg_objects(conf=self.configs)
        self.execute_pg_objects()

    def create_pg_objects(self, conf):

        env_keys = list(conf[0].keys())


        ### Spent way to long trying to do this elegantly, but you get the idea, I would have created a method that allowed the SQL to be generated based on
        ### the script and the environment, while reduceing code de duplication.

        for env in env_keys:

            dev_sql_create = users.keet_users.render(
                ENV=env,
                SCHEMA=conf[0][env]["SCHEMA"],
                DATABASE=conf[0][env]["DATABASE"],
                TABLE=conf[0][env]["TABLE"],
                ROLE=conf[0][env]["ROLE"]
            )

            self.sql_scripts.append(dev_sql_create)


            with open(os.path.dirname(__file__)[:-5] + "/sql_template/sql_ddl/users_env/users" + "_" + env.lower() + ".sql", 'w') as p:
                p.write(dev_sql_create)
            p.close()

            dev_sql_create_daily = users.keet_users.render(
                ENV=env,
                SCHEMA=conf[1][env]["SCHEMA"],
                DATABASE=conf[1][env]["DATABASE"],
                TABLE=conf[1][env]["TABLE"],
                ROLE=conf[1][env]["ROLE"]
            )

            self.sql_scripts.append(dev_sql_create_daily)

            with open(os.path.dirname(__file__)[:-5] + "/sql_template/sql_ddl/daily_users_env/daily_users_env" + "_" + env.lower() + ".sql",
                      'w') as p:
                p.write(dev_sql_create_daily)
            p.close()

    def execute_pg_objects(self):

        removed_newlines = list(map(lambda s: s.strip(), self.sql_scripts))
        clean_sql = list(filter(None, removed_newlines))

        conn = psycopg2.connect(database="dev_keet", user='postgres', password="epona27", host='localhost', port='5432')
        curr = conn.cursor()

        for sql in clean_sql:
            curr.execute(sql)

if __name__ == "__main__":
    L = Load()
    L.load_configs()
