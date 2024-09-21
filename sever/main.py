import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/test/")
async def send_home_israel_page() -> JSONResponse:
    return JSONResponse(content={"result": "true"}, status_code=200)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
