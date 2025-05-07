from typing import List, Optional
from sqlmodel import select
from models import *
from db import get_session
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

async def crear_usuario(datos: UsuarioCrear, session: AsyncSession) -> Usuario:
    nuevo = Usuario(**datos.dict())
    session.add(nuevo)
    await session.commit()
    await session.refresh(nuevo)
    return nuevo

async def obtener_todos(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario))
    return result.scalars().all()

async def obtener_uno(user_id: int, session: AsyncSession) -> Optional[Usuario]:
    return await session.get(Usuario, user_id)

async def actualizar_usuario(user_id: int, datos: UsuarioActualizar, session: AsyncSession) -> Optional[Usuario]:
    usuario = await obtener_uno(user_id, session)
    if usuario:
        if datos.premium is not None:
            usuario.premium = datos.premium
        if datos.activo is not None:
            usuario.activo = datos.activo
        session.add(usuario)
        await session.commit()
        await session.refresh(usuario)
    return usuario

async def usuarios_premium_activos(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(
        select(Usuario).where(Usuario.premium == True, Usuario.activo == True)
    )
    return result.scalars().all()

async def filtrar_usuarios(premium: Optional[bool], activo: Optional[bool], session: AsyncSession) -> List[Usuario]:
    query = select(Usuario)
    if premium is not None:
        query = query.where(Usuario.premium == premium)
    if activo is not None:
        query = query.where(Usuario.activo == activo)
    result = await session.execute(query)
    return result.scalars().all()

async def eliminar_usuario(id: int, session: AsyncSession):
    usuario = await session.get(Usuario, id)
    if not usuario:
        return None
    await session.delete(usuario)
    await session.commit()
    return usuario

async def crear_tarea(tarea: TareaCrear, session: AsyncSession):
    nueva = Tarea.from_orm(tarea)
    session.add(nueva)
    await session.commit()
    await session.refresh(nueva)
    return nueva

async def obtener_tareas(session: AsyncSession):
    resultado = await session.exec(select(Tarea))
    return resultado.all()

async def obtener_tarea(id: int, session: AsyncSession):
    return await session.get(Tarea, id)

async def actualizar_tarea(id: int, datos: TareaActualizar, session: AsyncSession):
    tarea = await session.get(Tarea, id)
    if not tarea:
        return None
    for k, v in datos.dict(exclude_unset=True).items():
        setattr(tarea, k, v)
    tarea.fecha_modificacion = datetime.utcnow()
    await session.commit()
    await session.refresh(tarea)
    return tarea

async def eliminar_tarea(id: int, session: AsyncSession):
    tarea = await session.get(Tarea, id)
    if not tarea:
        return None
    await session.delete(tarea)
    await session.commit()
    return tarea
