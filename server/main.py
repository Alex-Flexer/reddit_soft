import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse


app = FastAPI()


@app.post("/login/")
async def login() -> JSONResponse:
    pass


@app.post("/reg/")
async def reg() -> JSONResponse:
    pass


@app.post("/start-living/")
async def start_acount_living() -> JSONResponse:
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
