from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import config

MONTHS = [
    "Января",
    "Февраля",
    "Марта",
    "Апреля",
    "Мая",
    "Июня",
    "Июля",
    "Августа",
    "Сентября",
    "Октября",
    "Ноября",
    "Декабря"
]

app = FastAPI()

origins = [
    f"http://localhost:{config.APP_PORT}", f"https://localhost:{config.APP_PORT}",
    "http://localhost:2000", "https://localhost:2000",
    "http://127.0.0.1:2000", "https://127.0.0.1:2000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "content-disposition"
    ]
)

NOTIFY_ID = 231900398
