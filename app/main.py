import pandas as pd
from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
import pickle
from sklearn.neighbors import NearestNeighbors
from pydantic import BaseModel
import time
import numpy as np
from geopy.distance import geodesic

load_dotenv()
#for db configurations
a = os.getenv("NAME")
b = os.getenv("USER")
c = os.getenv("PASSWORD")
d = os.getenv("HOST", "db")
dbport = int(os.getenv("PORT"))

users = pd.read_parquet("./data/user.parquet")
restaurants = pd.read_parquet("./data/restaurant.parquet")

with open("./model.pkl", "rb") as f:
    model: NearestNeighbors = pickle.load(f)

async def rec(uid: str, lat: float, long: float, size: int, maxd: float, sortd: int):
    eucl, ind = model.kneighbors(users[users['user_id'] == uid].drop(columns="user_id"), n_neighbors=2000)

    #dis = time.time()
    rids = restaurants.iloc[ind[0]]['restaurant_id'].tolist()
    difference = eucl[0]
    #displacement = [geodesic((lat, long), (restaurants.iloc[i]['latitude'], restaurants.iloc[i]['longitude'])).meters for i in ind[0]]
    ulat = np.radians(lat)
    ulong = np.radians(long)
    restaurants["latitude"] = restaurants["latitude"].astype(float)
    restaurants["longitude"] = restaurants["longitude"].astype(float)
    rlat = np.radians(restaurants.iloc[ind[0]]['latitude'].values)
    rlong = np.radians(restaurants.iloc[ind[0]]['longitude'].values)
    earth_r = 6371000
    displacement = earth_r * np.arccos(np.sin(ulat) * np.sin(rlat) + np.cos(ulat) * np.cos(rlat) * np.cos(rlong - ulong)) #great circle
    out = [{"id": x, "difference": y, "displacement": z} for x, y, z in zip(rids, difference, displacement) if z <= maxd]
    #dis_time = time.time() - dis

    if sortd == 1:
        out.sort(key=lambda x: x["displacement"]) #sort by greatcircle
    else:
        out.sort(key=lambda x: x["difference"]) #sort by model
    #print(f"time: {dis_time:.3f}s")
    return out[:size]

class Recommendation(BaseModel):
    latitude: float
    longitude: float
    size: int = 20
    max_dis: float = 5000
    sort_dis: int = 0

app = FastAPI()

@app.get("/recommend/{user_id}")
async def getRec(user_id: str, latitude: float, longitude: float, size: int = Query(default = 20, ge = 1, le = 2000), 
           max_dis: float = Query(default = 5000, ge = 0), sort_dis: int = Query(default = 0, ge = 0, le = 1)):
    #if size is None:
    #    size = 20
    #if max_dis is None:
     #   max_dis = 5000
    #if sort_dis is None:
    #    sort_dis = 0
    return await rec(user_id, latitude, longitude, size, max_dis, sort_dis)

@app.post("/recommend/{user_id}")
async def postRec(user_id: str, r: Recommendation):
    return await rec(user_id, r.latitude, r.longitude, r.size, r.max_dis, r.sort_dis)

#@app.get("/")
#def read_root():
#    return {"message": "I NEED SLEEEEEP"}