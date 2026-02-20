# importaciones
from fastapi import FastAPI, status, HTTPException
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

@app.get("/v1/ParametroOb/{id}", tags=['Parametro obligatorio'])
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

@app.get("/v1/ParamtroOp/", tags=['Parametro opcional'])
async def consultatodos(id:Optional[int]=None):
    if id  is not None: 
        for usuarioK  in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK,
                        "status": "200"}
            
        return {"Mensaje": "Usuario no encontrado", "status": "200"}
    
    else:
        return {"menajes": "No se proporciono ids"}
            
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consutaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "Usarios": usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def agregar_usuario(usuario:dict):  ##usuarios, pero agregarlos como un diccionario
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code= 400, 
                detail="El id ya existe"
            )
    
    usuarios.append(usuario)
    return{
        "Mensaje": "Usuario agregado",
        "Usuario": usuario,
        "status": "200"
    }


##agregar put y delete

@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuario(usuario:dict):  ##usuarios, pero agregarlos como un diccionario
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr["nombre"] = usuario.get("nombre")
            usr["edad"] = usuario.get("edad")

            return {
                "Mensaje": "Usuario actualizado",
                "Usuario": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code= 404,
        detail="El usuario con ese ID no existe"
    )


@app.delete("/v1/usuarios/", tags=['CRUD HTTP'])
async def eliminar_usuario(usuario:dict):  ##usuarios, pero agregarlos como un diccionario
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.remove(usr)
            return {
                "Mensaje": "Usuario eliminado",
                "Usuario": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code= 404,
        detail="El usuario con ese ID no existe"
    )


