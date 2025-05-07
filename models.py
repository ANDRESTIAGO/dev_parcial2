from sqlmodel import SQLModel, Field
from typing import Optional

class UsuarioBase(SQLModel):
    nombre: str
    correo: str

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    premium: bool = False
    activo: bool = True

class UsuarioCrear(UsuarioBase):
    pass

class UsuarioActualizar(SQLModel):
    premium: Optional[bool] = None
    activo: Optional[bool] = None
