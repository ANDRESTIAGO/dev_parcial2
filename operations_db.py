from typing import List, Optional
from sqlmodel import select
from models import Usuario, UsuarioCrear, UsuarioActualizar
from db import get_session
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

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
