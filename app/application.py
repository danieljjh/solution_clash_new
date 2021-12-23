# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import FastAPI, Body, Form, UploadFile, File, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sclogic import Reaction


# :在这里建立了API
app = FastAPI()

origins = [
    'http://localhost:8080',
    'https://falltuna-project.github.io/'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
async def root():
    '''
    GET请求, 输入网址发送请求
    返回: JSON, {"message": "Hi cons"}
    '''
    return {"message": "Hi cons"}


@app.get("/generate_card_set")
async def gen_set():
    return ""
    