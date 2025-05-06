from fastapi import FastAPI, HTTPException
from typing import Optional, List
from models import UsuarioCrear, Usuario, UsuarioActualizar
import operations_db as funciones

app = FastAPI(title="API Local de Usuarios", docs_url="/docs")

@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCrear):
    return funciones.crear_usuario(usuario)

@app.get("/usuarios/", response_model=List[Usuario])
def leer_usuarios():
    return funciones.obtener_todos()

@app.get("/usuarios_premium/", response_model=List[Usuario])
def leer_premium():
    return funciones.usuarios_premium_activos()

@app.get("/usuarios/{user_id}", response_model=Usuario)
def leer_usuario(user_id: int):
    usuario = funciones.obtener_uno(user_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, datos: UsuarioActualizar):
    usuario = funciones.actualizar_usuario(user_id, datos)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/activos-premium", response_model=List[Usuario])
def obtener_premium_activos():
    return funciones.usuarios_premium_activos()

@app.get("/usuarios/filtrar", response_model=List[Usuario])
def filtrar(premium: Optional[bool] = None, activo: Optional[bool] = None):
    return funciones.filtrar_usuarios(premium, activo)
