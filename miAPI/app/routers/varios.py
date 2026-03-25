from app.data.database import usuarios
import asyncio 
from typing import Optional
from fastapi import APIRouter

routerV = APIRouter(
    tags=['Inicio']
)


@routerV.get("/")
async def Bievenvido():
    return {"mensaje":"Bienvenido a FastAPI",
            }


@routerV.get("/holaMundo")
async def Hola():
    await asyncio.sleep(5)  #peticion, consultaBD, Archivo
    return {"mensaje":"Hola Mundo FastAPI",
            "status":"200"
            }


@routerV.get("/v1/ParametroOb/{id}")
async def consultauno(id:int):
    return {"mensaje":"Usario encontrado",
            "usuario": id,
            "status": "200"
            }


@routerV.get("/v1/ParamtroOp/")
async def consultatodos(id:Optional[int]=None):
    if id  is not None: 
        for usuario_k  in usuarios:
            if usuario_k["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario_k,
                        "status": "200"}
            
        return {"Mensaje": "Usuario no encontrado", "status": "200"}
    
    else:
        return {"menajes": "No se proporciono ids"}
            

