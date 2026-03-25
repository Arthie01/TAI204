from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional, Annotated
import secrets ##manipulacion de contraseñas hasehadas
from fastapi import FastAPI, status, HTTPException, Depends

### Seguridad con HTTP BASIC
security = HTTPBasic()

def verificar_peticion(credenciales: Annotated[HTTPBasicCredentials, Depends(security)]):
    usuario_aut= secrets.compare_digest(credenciales.username, "artemio")
    contra_aut= secrets.compare_digest(credenciales.password, "123456")

    if not(usuario_aut and contra_aut):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no autorizadas"
        )
    
    return credenciales.username
