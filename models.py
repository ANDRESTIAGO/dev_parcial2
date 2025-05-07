from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

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

class Tarea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_modificacion: datetime = Field(default_factory=datetime.utcnow)
    estado: str  # Pendiente, En ejecución, Realizada, Cancelada
    usuario_id: int = Field(foreign_key="usuario.id")

class TareaCrear(SQLModel):
    nombre: str
    descripcion: str
    estado: str 
    usuario_id: int

class TareaActualizar(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
