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

class tipo_Tramite(str, Enum):
    deposito = "deposito"
    retiro = "retiro"
    consulta = "consulta"


class crear_turno(BaseModel):
    id: int = Field(..., gt=0)
    cliente: str =Field(...,min_length=3, max_length=8)
    turno: datetime = Field(...)

turnos = [
    
]


@app.post("/crearTurno/")
async def crear_turno(turno: crear_turno):
    today = datetime.now()

    for tur in turnos:
        if tur["id"] == turno.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La reserva ya existe"
            )
        if today.hour <= 9 or today.hour>=3:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="NO se puede crear citas a esa hora"
            )
        if today.hour >= 9 or today.hour<=3:
            turnos.append(turno.model_dump())
            return{
                "Mensaje": "Cita creada",
                "Reserva": turno,
                "status": "200"
            }

@app.get("/listarTurnos/")
async def listarTurnos(turno:)










