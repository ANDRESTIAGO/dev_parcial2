from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    correo: str

class UsuarioCrear(UsuarioBase):
    pass

class UsuarioActualizar(BaseModel):
    premium: bool | None = None
    activo: bool | None = None

class Usuario(UsuarioBase):
    id: int
    premium: bool
    activo: bool
