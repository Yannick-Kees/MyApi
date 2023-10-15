# uvicorn main:app --reload
from fastapi import FastAPI
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import csv

app = FastAPI()
DATABASE = "database.csv"

class Post(BaseModel):
    movie: str
    date: str 
    rating: str


def get_data_from_csv(path = DATABASE):
    data_list = []

    with open(path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            data_list.append(dict(row))
    
    return data_list

def find_post(id):
    database = get_data_from_csv()
    
    for p in database:
        print(p["id"], id)
        print(type(p["id"]), type(id))
        if int(p['id']) == int(id):
            print("hex")
            return p
        
def new_id():
    ids = []
    for p in get_data_from_csv():
        print(p["id"])
        ids.append(int(p["id"]))
    return str(max(ids) + 1 )

@app.get("/")
async def root():
    return {"message": "hello!!"}

@app.get("/movies")
def get_movies():
    data = get_data_from_csv()
    return {"data": data}

@app.post("/movies")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = new_id()
    with open(DATABASE, 'a', newline='') as csvfile:
        fieldnames = post_dict.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the CSV file is empty and needs headers
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(post_dict)
    
    return {"data": post_dict}

@app.get("/movie/{id}")
def get_post(id):
    
    post = find_post(id)
    return {"data" : post}
    
