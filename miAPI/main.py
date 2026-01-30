# importaciones
from fastapi import FastAPI
import asyncio 

#Instancia del servidor

app = FastAPI()

#endpoints


@app.get("/")
async def Bievenvido():
    return {"mensaje":"Bienvenido a FastAPI",
            }


@app.get("/holaMundo")
async def Hola():
    await asyncio.sleep(5)  #peticion, consultaBD, Archivo
    return {"mensaje":"Hola Mundo FastAPI",
            "status":"200"
            }

