from models import Usuario, UsuarioCrear, UsuarioActualizar
from typing import List, Optional
import csv
import os

ARCHIVO_CSV = "usuarios.csv"
CAMPOS = ["id", "nombre", "correo", "premium", "activo"]

def cargar_usuarios() -> List[Usuario]:
    usuarios = []
    if os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                usuarios.append(Usuario(
                    id=int(fila["id"]),
                    nombre=fila["nombre"],
                    correo=fila["correo"],
                    premium=fila["premium"].lower() == "true",
                    activo=fila["activo"].lower() == "true"
                ))
    return usuarios

def guardar_usuarios(usuarios: List[Usuario]):
    with open(ARCHIVO_CSV, "w", newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        escritor.writeheader()
        for u in usuarios:
            escritor.writerow({
                "id": u.id,
                "nombre": u.nombre,
                "correo": u.correo,
                "premium": u.premium,
                "activo": u.activo
            })

usuarios_db: List[Usuario] = cargar_usuarios()
contador_id = max((u.id for u in usuarios_db), default=0) + 1

def crear_usuario(datos: UsuarioCrear) -> Usuario:
    global contador_id
    nuevo = Usuario(id=contador_id, premium=False, activo=True, **datos.dict())
    usuarios_db.append(nuevo)
    guardar_usuarios(usuarios_db)
    contador_id += 1
    return nuevo

def obtener_todos() -> List[Usuario]:
    return usuarios_db

def obtener_uno(user_id: int) -> Optional[Usuario]:
    return next((u for u in usuarios_db if u.id == user_id), None)

def actualizar_usuario(user_id: int, datos: UsuarioActualizar) -> Optional[Usuario]:
    usuario = obtener_uno(user_id)
    if usuario:
        if datos.premium is not None:
            usuario.premium = datos.premium
        if datos.activo is not None:
            usuario.activo = datos.activo
        guardar_usuarios(usuarios_db)
    return usuario

def usuarios_premium_activos() -> List[Usuario]:
    usuarios = leer_usuarios_csv()
    return [u for u in usuarios if u.premium and u.activo]

def filtrar_usuarios(premium: Optional[bool], activo: Optional[bool]) -> List[Usuario]:
    resultado = usuarios_db
    if premium is not None:
        resultado = [u for u in resultado if u.premium == premium]
    if activo is not None:
        resultado = [u for u in resultado if u.activo == activo]
    return resultado

def leer_usuarios_csv() -> List[Usuario]:
    usuarios = []
    if os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode="r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                usuarios.append(
                    Usuario(
                        id=int(fila["id"]),
                        nombre=fila["nombre"],
                        correo=fila["correo"],
                        premium=fila["premium"].lower() == "true",
                        activo=fila["activo"].lower() == "true"
                    )
                )
    return usuarios
