# from requests import post, get
# from json import dumps

# data = dumps({"email": "some email", "password": "123"})
# res = post("http://127.0.0.1:8000/sign-up/user", data=data)
# print(res.json())
# print()

import database.database_functions as db


db.delete_user_by_email("sasha.flexer@gmail.com")