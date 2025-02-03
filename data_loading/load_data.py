import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() #added this for security dont forget to explain in readme

def create_table(cursor):
    """Create the restaurants table if it doesn't exist"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            restaurant_id TEXT PRIMARY KEY,
            index INTEGER,
            latitude FLOAT,
            longitude FLOAT
        );
    """)

def load_restaurants():
    res = pd.read_parquet('./data/restaurant.parquet')
    a = os.getenv("NAME")
    b = os.getenv("USER")
    c = os.getenv("PASSWORD")
    d= os.getenv("HOST", "db")
    e= os.getenv("PORT")
    con= psycopg2.connect(dbname=a,
                            user=b, 
                            password=c, 
                            host=d, 
                            port=e)
    cursor=con.cursor()
    create_table(cursor)
    for x, y in res.iterrows():
        cursor.execute(
            """
            INSERT INTO restaurants (restaurant_id, index, latitude, longitude) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (restaurant_id) DO NOTHING;
            """,
            (y['restaurant_id'], y['index'], y['latitude'], y['longitude'])
        )

    con.commit()
    cursor.close()
    con.close()
if __name__ == "__main__":
    load_restaurants()