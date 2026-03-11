# importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio 
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from enum import Enum
import secrets ##manipulacion de contraseñas hasehadas
from datetime import datetime

app = FastAPI()

security = HTTPBasic()

def verificar_peticion(credenciales: Annotated[HTTPBasicCredentials, Depends(security)]):
    usuario_aut= secrets.compare_digest(credenciales.username, "banco")
    contra_aut= secrets.compare_digest(credenciales.password, "2468")

    if not(usuario_aut and contra_aut):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no autorizadas"
        )
    
    return credenciales.username

class tipo_Tramite(str, Enum):
    deposito = "deposito"
    retiro = "retiro"
    consulta = "consulta"

class atendidoTurno(str, Enum):
    atendio ="atendido"
    noAtendido = "no atendido"


class crear_turno(BaseModel):
    id: int = Field(..., gt=0)
    cliente: str =Field(...,min_length=3, max_length=8)
    turno: datetime = Field(...)
    Atendido: atendidoTurno =Field(...)

turnos = [
    {"id":1, "cliente":"artemio", "turno":"9:30"}
]


@app.post("/crearTurno/")
async def crear_turno(turno: crear_turno):
    today = datetime.hour()

    for tur in turnos:
        if tur["id"] == turno.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La reserva ya existe"
            )
        if today >= 9 or today<=3:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="NO se puede crear citas a esa hora"
            )
        if today <= 9 or today>=3:
            turnos.append(turno.model_dump())
            return{
                "Mensaje": "Cita creada",
                "Reserva": turno,
                "status": "200"
            }

@app.get("/listarTurnos/")
async def listarTurnos():
    return{
        "status":"200",
        "total":len(turnos),
        "turno": turnos
    }


@app.get("/turno/{turno_id}/")
async def buscar_libro(turno_id:int):
    for turn in turnos:
        if turn["id"] == turno_id:
            return{
                "Mensaje": "Turno obtenido",
                "Turno": turn,
                "status": "200"
            }


@app.patch("/Atendido/{turno.id}/atendido")
async def MarcarAtendido(turno_id: int):
    turno_atendido = False
    for turn in turnos:
        if turn["id"] == turno_id:
            if turn["Atendido"] != "atendido":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="YA FUE ATENDIDO"
                )
            
            turn["Atendido"]: "atendido"
            turn["Atendido"]: turno_id


    if not turno_atendido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EL turno con ese ID no existe"  
        )
    
@app.delete("/eliminar/{turno_id}/")
async def eliminar_turno(turno_id:int):
    for i, turn in enumerate(turnos):
        if turn["id"] == turno_id:
            turno_eliminado = turnos.pop(i)
            return{
                "Mensaje": "Turno eliminado",
                "Turno": turno_eliminado,
                "status": "200"
            }
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail="Turno eliminado"
    )









