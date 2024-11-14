import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from keyring import get_password as get_secret_value

from random import random

from functions.check_transaction import check_transaction
from functions.authorization_code_sender import send_code
import database.database_functions as db
from server.database.database_functions import update_user_token

app = FastAPI()

app.mount(
    path="/static",
    app=StaticFiles(directory="../server/static", html=True),
    name="static"
)


@app.get("/")
async def send_home_page() -> FileResponse:
    return FileResponse("../server/static/html/index.html")


@app.get("/sign-up/")
async def send_registration_page() -> FileResponse:
    return FileResponse("../server/static/html/sign_up.html")


@app.get("/confirm-code/")
async def check_email_code() -> FileResponse:
    return FileResponse("../server/static/html/check_email_code.html")


@app.get("/login/")
async def send_login_page() -> FileResponse:
    return FileResponse("../server/static/html/login.html")


@app.get("/tariffs/")
async def send_tariffs() -> FileResponse:
    return FileResponse("../server/static/html/tariffs.html")


@app.get("/buy-form/")
async def send_buy_form() -> FileResponse:
    return FileResponse("../server/static/html/buy_form.html")


@app.get("/successful-purchase/")
async def send_purchase_page() -> FileResponse:
    return FileResponse("../server/static/html/successful_purchase.html")


@app.get("/get/installer")
async def send_installer() -> FileResponse:
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}

    return FileResponse(
        "../server/private_resources/installer.py", filename="RS-installer.py", headers=headers)


@app.get("/get/instruction")
async def send_instruction() -> FileResponse:
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}

    return FileResponse(
        "../server/private_resources/instruction.pdf", filename="RS-instruction.pdf", headers=headers)


@app.post("/get/software")
async def send_software(request: Request) -> FileResponse:
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}

    json: dict = await request.json()
    status_code = 400

    if {"email", "password", "token"}.issubset(json.keys()):
        email = json["email"]
        password = json["password"]
        token = json["token"]

        if db.check_user_exists(email):
            is_valid_user_credentials = db.check_user_credentials(email, password, token)

            status_code = 200 if is_valid_user_credentials else 403
        else:
            status_code = 404

    if status_code == 200:
        return FileResponse(
            "../server/private_resources/source.zip", filename="RedditSyndicate.zip", status_code=200, headers=headers)
    else:
        return FileResponse("../server/private_resources/empty.txt", status_code=status_code, headers=headers)


@app.post("/sign-up/user/")
async def add_user(request: Request) -> JSONResponse:
    json = await request.json()

    response_json = {"result": False, "message": "Incorrect request"}

    if {"email", "password"}.issubset(json.keys()):
        email = json["email"]
        password = json["password"]

        if db.check_user_exists(email):
            response_json["message"] = "User already exists"
        else:
            result = db.add_new_user(email, password)
            if result:
                response_json["message"] = ""
                response_json["result"] = True
            else:
                response_json["message"] = "Unknown sing up error"

    return JSONResponse(content=response_json, status_code=200)


@app.post("/login/user/")
async def login_user(request: Request) -> JSONResponse:
    json = await request.json()

    response_json = {"result": False, "message": "Incorrect request"}

    if {"email", "password"}.issubset(json.keys()):
        email = json["email"]
        password = json["password"]

        if not db.check_user_exists(email):
            response_json["message"] = "User with this email does not exist"
        elif not db.check_user_confirmed(email):
            response_json["message"] = "Registration email code not confirmed"
        elif not db.check_user_password(email, password):
            response_json["message"] = "Incorrect password"
        else:
            response_json["result"] = True
            response_json["message"] = ""

    return JSONResponse(content=response_json, status_code=200)


@app.post("/confirm/email-code")
async def check_user_code(request: Request) -> JSONResponse:
    json = await request.json()

    response_json = {
        "result": False,
        "message": "Incorrect request"
    }

    if {"email", "code"}.issubset(json.keys()):
        email = json["email"]
        code = json["code"]

        if not db.check_user_exists(email):
            response_json["message"] = "User with this email does not exist"
        elif not db.check_authorization_code(email, code):
            response_json["message"] = "Incorrect authorization code"
        else:
            db.confirm_email_code(email)
            response_json["message"] = ""
            response_json["result"] = True

    return JSONResponse(content=response_json, status_code=200)


@app.post("/send/email-code/")
async def send_email_code(request: Request) -> JSONResponse:
    json = await request.json()
    response_json = {"result": False, "message": "Incorrect request"}

    if {"email"}.issubset(json.keys()):
        response_json["result"] = True
        response_json["message"] = ""

        email = json["email"]
        code = send_code(email)

        db.update_email_code(email, code)

    return JSONResponse(content=response_json, status_code=200)


@app.post("/update/user-token/")
async def send_email_code(request: Request) -> JSONResponse:
    json = await request.json()
    response_json = {"result": False, "message": "Incorrect request", "token": None}
    
    if {"email"}.issubset(json.keys()):
        email = json["email"]

        if not db.check_user_exists(email):
            response_json["message"] = "User with this email does not exist"
        else:
            new_token = update_user_token(email)

            response_json["result"] = True
            response_json["message"] = ""
            response_json["token"] = new_token

    return JSONResponse(content=response_json, status_code=200)


@app.post("/check/transaction/")
async def check_user_transaction(request: Request) -> JSONResponse:
    json: dict = await request.json()
    response_json = {"result": False, "message": "Incorrect request"}

    if {"email"}.issubset(json.keys()):
        email = json["email"]

        if db.check_user_exists(email):
            try:
                price = db.get_user_active_subscription_price(email)
                transaction_verdict = check_transaction(price)
            except Exception as e:
                response_json["message"] = "Unknown checking transaction Error"
                print(e)
            else:
                if transaction_verdict:
                    db.renew_subscription(email)
                    response_json["result"] = True
                    response_json["message"] = ""
                else:
                    response_json["message"] = "Transaction was not found"
        else:
            response_json["message"] = "Users with this email does not exists"

    return JSONResponse(content=response_json, status_code=200)


@app.post("/check/user-credentials/")
async def check_user_credentials(request: Request) -> JSONResponse:
    json: dict = await request.json()
    response_json = {"result": False, "message": "Incorrect request"}

    if {"email", "password", "token"}.issubset(json.keys()):
        email = json["email"]
        password = json["password"]
        token = json["token"]

        if db.check_user_exists(email):
            is_valid_user_data = db.check_user_credentials(email, password, token)
            if not is_valid_user_data:
                response_json["message"] = "Incorrect credentials"
            else:
                response_json["result"] = True
                response_json["message"] = ""
        else:
            response_json["message"] = "Users with this email does not exists"

    return JSONResponse(content=response_json, status_code=200)


@app.post("/get/price/")
async def send_price(request: Request) -> JSONResponse:
    json: dict = await request.json()
    response_json: dict = {"result": False, "message": "Incorrect request"}

    if {"email", "price"}.issubset(json.keys()):
        email = json["email"]
        price = json["price"]
        new_price = price + round(random(), 3)

        db.update_subscription_price(email, new_price)

        response_json["result"] = True
        response_json["price"] = new_price
        response_json["message"] = ""

    return JSONResponse(content=response_json, status_code=200)


@app.get("/get/crypto-token/")
async def send_crupto_token() -> JSONResponse:
    response_json: dict = {"result": False, "message": "Crytotoken was not found"}

    crypto_token = get_secret_value("common", "CRYPTO_TOKEN")

    if not crypto_token is None:
        response_json["result"] = True
        response_json["token"] = crypto_token
        response_json["message"] = ""

    return JSONResponse(content=response_json, status_code=200)


@app.post("/add/reddit-account/")
async def send_price(request: Request) -> JSONResponse:
    json: dict = await request.json()
    response_json: dict = {"result": False, "message": "Incorrect request"}

    if {"email", "price"}.issubset(json.keys()):
        email = json["email"]
        price = json["price"]
        new_price = price + round(random(), 3)

        db.update_subscription_price(email, new_price)

        response_json["result"] = True
        response_json["price"] = new_price
        response_json["message"] = ""

    return JSONResponse(content=response_json, status_code=200)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
