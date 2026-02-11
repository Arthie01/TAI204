# importaciones
from fastapi import FastAPI
import asyncio 
from typing import Optional

#Instancia del servidor

app = FastAPI (
    title = "MI primera API",
    description= "Artemio Hurtado Hernandez",
    version="1.0"
    )




#endpoint

@app.get("/", tags=['Inicio'])
async def Bievenvido():
    return {"mensaje":"Bienvenido a FastAPI",
            }


@app.get("/holaMundo", tags=['Asincronia'])
async def Hola():
    await asyncio.sleep(5)  #peticion, consultaBD, Archivo
    return {"mensaje":"Hola Mundo FastAPI",
            "status":"200"
            }

@app.get("/v1/usuario/{id}", tags=['Parametro obligatorio'])
async def consultauno(id:int):
    return {"mensaje":"Usario encontrado",
            "usuario": id,
            "status": "200"
            }

usuarios = [
    {"id":1, "nombre": "Artemio", "edad": "21"},
    {"id":2, "nombre": "RIcardo", "edad": "22"},
    {"id":3, "nombre": "Emilio", "edad": "25"}
]

@app.get("/v1/usuarios/", tags=['Parametro opcional'])
async def consultatodos(id:Optional[int]=None):
    if id  is not None: 
        for usuarioK  in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK,
                        "status": "200"}
            
        return {"Mensaje": "Usuario no encontrado", "status": "200"}
    
    else:
        return {"menajes": "No se proporciono ids"}
            

