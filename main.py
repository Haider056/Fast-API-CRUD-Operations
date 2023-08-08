from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from fastapi import FastAPI, Request, status, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Pydantic model for the request body
class PostData(BaseModel):
    title: str
    content: str

# Function to establish a connection to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="AR",
            user="postgres",
            password="1234"
        )
        print("Connected to the database")
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Route to insert data into the database
@app.post("/insertdata")
def insert_data_to_db(data: PostData):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO prog (title, content) VALUES (%s, %s)"
            cursor.execute(query, (data.title, data.content))
            connection.commit()
            cursor.close()
            print("Data inserted successfully.")
            return {"message": "Data inserted successfully."}
        except psycopg2.Error as e:
            print("Error inserting data:", e)
            raise HTTPException(status_code=500, detail="Error inserting data")
        finally:
            connection.close()


def fetch_data():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT id, title, content FROM prog"
            cursor.execute(query)
            fetched_data = cursor.fetchall()
            cursor.close()
            return fetched_data
        except psycopg2.Error as e:
            print("Error fetching data:", e)
            return []
        finally:
            connection.close()

# Route to fetch data from the database
@app.get("/fetchdata")
def get_data_from_db():
    data = fetch_data()
    return {"data": data}


@app.put("/updatedata/{id}")
def update_data_in_db(id: int, data: PostData):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE prog SET title = %s, content = %s WHERE id = %s"
            cursor.execute(query, (data.title, data.content, id))
            connection.commit()
            cursor.close()
            print("Data updated successfully.")
            return {"message": "Data updated successfully."}
        except psycopg2.Error as e:
            print("Error updating data:", e)
            raise HTTPException(status_code=500, detail="Error updating data")
        finally:
            connection.close()
def fetch_all_data():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT id, title, content FROM prog"
            cursor.execute(query)
            fetched_data = cursor.fetchall()
            cursor.close()
            return fetched_data
        except psycopg2.Error as e:
            print("Error fetching all data:", e)
            return []
        finally:
            connection.close()

# Route to fetch all data from the database
@app.get("/getall")
def get_all_data():
    data = fetch_all_data()
    return {"data": data}

@app.delete("/deletedata/{id}")
def delete_data_from_db(id: int):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM prog WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            cursor.close()
            print("Data deleted successfully.")
            return {"message": "Data deleted successfully."}
        except psycopg2.Error as e:
            print("Error deleting data:", e)
            raise HTTPException(status_code=500, detail="Error deleting data")
        finally:
            connection.close()


@app.get("/")
def root():
    return {"Hello": "World"}

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "I like pizza", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        

def find_post_by_id(post_id):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None

@app.get("/root1")
def root1():
    return {"Post hello"}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    parameters: int = 61

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"detail": post}

@app.post("/route2")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": my_posts}  # Return the updated list of all posts

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post_by_id(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id:int):
    index=find_index_post(id)
    
    my_posts.pop(index)
    return{'message':'post was deleted'}
@app.put("/posts/{id}")
def update_post(id:int,post: Post):
  index=find_index_post(id)
  
  if index==None:
   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

  post_dict=post.dict()
  post_dict['id']=id
  my_posts[index]=post_dict
  return{"data":post_dict}