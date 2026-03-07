from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import asyncio
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY = "Lo que hay aqui dentro es lo mas secreto de lo secreto de todo lo secreto y yo soy el unico testigo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

USERS_DB = {
    "artemio": {"username": "artemio", "password": "123456"}
}

app = FastAPI(
    title = "MI primera API",
    description= "Artemio Hurtado Hernandez",
    version="2.0"
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )


@app.post("/token", tags=["Autenticacion"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = USERS_DB.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = crear_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", tags=['Inicio'])
async def Bievenvido():
    return {"mensaje":"Bienvenido a FastAPI",
            }


@app.get("/holaMundo", tags=['Asincronia'])
async def Hola():
    await asyncio.sleep(5)
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

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example= "pepe pecas")
    edad: int = Field(..., ge=1, le=125, description= "Edad valida entre 1 y 125")


@app.get("/v1/ParamtroOp/", tags=['Parametro opcional'])
async def consultatodos(id:Optional[int]=None):
    if id  is not None: 
        for usuario_k  in usuarios:
            if usuario_k["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario_k,
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
async def agregar_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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


@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuario(usuario: dict, usuario_aut: Annotated[str, Depends(verificar_token)]):
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


@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuario_aut: Annotated[str, Depends(verificar_token)]):
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


