# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import FastAPI, Body, Form, UploadFile, File, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sclogic import Player, Beaker
from cardset import *
import random

# p1comb = ["HCl", "AgCl", "CuSO4.5H2O", "CaCO3",
#           "NaOH", "Ca(OH)2", "BaSO4", "NaCl"]
# c1 = [3, 1, 4, 2, 3, 5, 2, 1]
# p2comb = ["HCl", "AgCl", "CuSO4", "CaCO3",
#           "H2S", "Ca(OH)2", "H2SO4", "NH3.H2O"]
# c2 = [3, 1, 3, 2, 2, 5, 5, 2]


def form_card_seq():
    cardseq = []
    seq = random.choices(cardset, k=8)
    # for i in range(8):
    #     item_dict = {"name": cardset[i], "no": seq[i], "cost": cseq[i]}
    #     cardseq.append(item_dict)
    for i in range(8):
        cardseq.append(cardset[i])
    return cardseq


# :在这里建立了API
app = FastAPI()

origins = [
    'http://localhost:8080',
    'https://falltuna-project.github.io/'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    '''
    GET请求, 输入网址发送请求
    返回: JSON, {"message": "Hi cons"}
    '''
    return {"message": "Hi cons"}


@app.post("/init_cards")
async def gen_set():
    p1seq = form_card_seq()
    p2seq = form_card_seq()
    return {'cards': [p1seq, p2seq]}


@app.post("/react")
async def react(
    score=Body(...),
    water=Body(...),
    beaker=Body(...),
    card=Body(...)
):
    # bIons是符合sclogic中beaker输入数据的
    bIons = {}
    for i in range(len(beaker)):
        p = list(beaker[i].values())
        # bIons[p[0]]=int(p[1])
        bIons.update({p[0]: p[1]})
    Player1 = Player("", "")
    B = Beaker(score, water, bIons, Player1)
    B.ioni(str(card["name"]))
    rIons = []
    for k, v in B.Ions.items():
        rIons.append({
            'name': k,
            'quantity': v
        })
    # rIon_list = list(B.Ions.keys())
    # rIon_val = list(B.Ions.values())
    # for i in range(len(rIon_val)):
    #     ion = {"name": rIon_list[i],"quantity": rIon_val[i]}
    #     rIons.append(ion)
    return {
        "score": B.cH,
        "water": B.water,
        "beaker": rIons,
        "displays": B.evalue,
        "pH": B.pH
    }
