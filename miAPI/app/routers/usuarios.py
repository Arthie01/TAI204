from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion
from sqlalchemy.orm import session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB
import asyncio 
from typing import Optional, Annotated


router = APIRouter(
    prefix = "/v1/usuarios", tags=['CRUD HTTP']
)



@router.get("/")
async def consutaT(db: Annotated[session, Depends(get_db)]):
    query_usuario = db.query(UsuarioDB).all()
    return{
        "status": "200",
        "total": len(query_usuario),
        "Usarios": query_usuario
    }

@router.post("/")
async def agregar_usuario(usuarioP:crear_usuario, db: Annotated[session, Depends(get_db)]):  ##usuarios, pero agregarlos como un diccionario

    usuarioNuevo = UsuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)

    return{
        "Mensaje": "Usuario agregado",
        "Usuario": usuarioP,
        "status": "200"
    }


##agregar put y delete

@router.put("/")
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


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuario_aut: Annotated[str, Depends(verificar_peticion)]):
    for usr in usuarios:
        if usr["id"] == id:
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



