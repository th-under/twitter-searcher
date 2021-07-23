
import time
from sqlalchemy import create_engine
import pandas as pd
import os

# postgres credentials and initialization
UNAME = "postgres"
PWD = "1234"
HOST = "my_postgres"
PORT = "5432"
DB = "postgres"

INTERVALL = int(os.getenv('EVAL_INTERVALL'))


pg = create_engine(f"postgresql://{UNAME}:{PWD}@{HOST}:{PORT}/{DB}")


# delay in reading to avoid race condition
time.sleep(INTERVALL)

# read from sql database

out_tweets = pd.read_sql("SELECT * FROM ttweets;", pg)


with open('evaluate.csv','w') as debugging:
    debugging.write(out_tweets.to_csv())
    
# to refrain container from exiting
while True:
    time.sleep(10)