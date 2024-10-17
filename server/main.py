import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
import data_base_functions as db
from server.data_base_functions import check_user_password

app = FastAPI()


@app.post("/login/")
async def login(request: Request) -> JSONResponse:
    json = await request.json()

    email = json["email"]
    password = json["password"]

    response_content = {"message": "User was successfully logged in."}

    if not db.check_user_exists(email):
        response_content["message"] = "User already exists"
    elif not check_user_password(email, password):
        response_content["message"] = "Incorrect password"

    return JSONResponse(content=response_content, status_code=200)


@app.post("/sing-up/")
async def sing_up(request: Request) -> JSONResponse:
    json = await request.json()

    email = json["email"]
    user_password = json["user_password"]
    reddit_password = json["reddit_password"]

    response_content = {"message": "User was successfully registered"}

    if db.check_user_exists(email):
        response_content = {"message": "User already exists"}
    else:
        was_user_added = db.add_new_user(email, user_password, reddit_password)
        if not was_user_added:
            response_content["message"] = "Something went wrong"

    return JSONResponse(content=response_content, status_code=200)


@app.post("/start-farming-carma/")
async def start_farming_carma() -> JSONResponse:
    pass


@app.post("/uniqueize-video/")
async def video_uniqueizer() -> FileResponse:
    pass


@app.post("/convert-photo/")
async def convert_photo() -> FileResponse:
    pass


@app.post("/convert-video/")
async def convert_video() -> FileResponse:
    pass


@app.post("/uniqueize-photo/")
async def photo_uniqueizer() -> FileResponse:
    pass


@app.post("/download-reals/")
async def download_reals() -> FileResponse:
    pass


@app.post("/download-shorts/")
async def download_shorts() -> FileResponse:
    pass


@app.post("/download-tiktok/")
async def download_tiktok() -> FileResponse:
    pass


@app.post("/check-transaction/")
async def check_transaction() -> JSONResponse:
    pass


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
