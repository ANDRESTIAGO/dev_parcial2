from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from models import UsuarioCrear, Usuario, UsuarioActualizar
from db import get_session
import operations_db as funciones

app = FastAPI(title="API Local de Usuarios", docs_url="/docs")

@app.post("/usuarios/", response_model=Usuario)
async def crear(usuario: UsuarioCrear, session: AsyncSession = Depends(get_session)):
    return await funciones.crear_usuario(usuario, session)

@app.get("/usuarios/", response_model=List[Usuario])
async def leer_todos(session: AsyncSession = Depends(get_session)):
    return await funciones.obtener_todos(session)

@app.get("/usuarios/{user_id}", response_model=Usuario)
async def leer_uno(user_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await funciones.obtener_uno(user_id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{user_id}", response_model=Usuario)
async def actualizar(user_id: int, datos: UsuarioActualizar, session: AsyncSession = Depends(get_session)):
    usuario = await funciones.actualizar_usuario(user_id, datos, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/activos-premium", response_model=List[Usuario])
async def obtener_activos_premium(session: AsyncSession = Depends(get_session)):
    return await funciones.usuarios_premium_activos(session)

@app.get("/usuarios/filtrar", response_model=List[Usuario])
async def filtrar(
    premium: Optional[bool] = None,
    activo: Optional[bool] = None,
    session: AsyncSession = Depends(get_session)
):
    return await funciones.filtrar_usuarios(premium, activo, session)
