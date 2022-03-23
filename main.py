from fastapi import FastAPI, Body
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: Optional[int] = 0
    name: str
    email: str
    phone: Optional[str] = None


fake_users_db = [
    User(id=1, name='rafael', email='crdm.rafael@gmail.com', phone='(21)99999-9999'),
    User(id=2, name='gabriel', email='gabriel@gmail.com'),
]


@app.get('/')
async def root():
    return {'message': 'First time using FastAPI'}


@app.get('/users/{user_id}')
def read(user_id: int):
    return {'user': [user for user in fake_users_db if user.id == user_id]}


@app.get('/users/')
async def read_pagination(skip: int = 0, limit: int = 10):
    return {'users': fake_users_db[skip: skip + limit]}


# Rota para criação com validação
@app.post('/users')
def create_user(user: User):
    user.id = fake_users_db[-1].id + 1
    fake_users_db.append(user)
    return {'message': 'User was created!'}


# Rota para criação sem validação
# @app.post('/any')
# def create_any(body=Body(...)):
#     return {'body': body}


@app.patch('/users/{user_id}')
def update(user_id: int, user: User):
    index = [index for index, user in enumerate(fake_users_db) if user.id == user_id]
    user.id = fake_users_db[index[0]].id
    fake_users_db[index[0]] = user
    return {'message': 'User was updated!'}


@app.delete('/users/{user_id}')
def delete(user_id: int):
    user = [user for user in fake_users_db if user.id == user_id]
    fake_users_db.remove(user[0])
    return {'message': 'User was deleted!'}
