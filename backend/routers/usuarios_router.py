from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database.connection import get_db_connection

router = APIRouter(prefix="/api/usuarios", tags=["Gestión de Usuarios"])

# Modelo corregido para permitir registro flexible desde la web
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password_hash: Optional[str] = "default_hash"
    id_rol: Optional[int] = 1

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    id_rol: Optional[int] = None

@router.get("/")
def listar_usuarios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID_USUARIO, NOMBRE, EMAIL, PASSWORD_HASH, ID_ROL, FECHA_CREACION 
            FROM USUARIOS
        """)
        rows = cursor.fetchall()
        
        usuarios = []
        for row in rows:
            usuarios.append({
                "id_usuario": row[0],
                "nombre": row[1],
                "email": row[2],
                "password_hash": row[3],
                "id_rol": row[4],
                "fecha_creacion": str(row[5]) if row[5] else None
            })
            
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_usuario(usuario: UsuarioCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO USUARIOS (NOMBRE, EMAIL, PASSWORD_HASH, ID_ROL)
            VALUES (:1, :2, :3, :4)
        """
        cursor.execute(sql, (
            usuario.nombre, 
            usuario.email, 
            usuario.password_hash, 
            usuario.id_rol
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "¡Usuario creado exitosamente!", "usuario": usuario}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE USUARIOS 
            SET NOMBRE = COALESCE(:1, NOMBRE),
                EMAIL = COALESCE(:2, EMAIL),
                PASSWORD_HASH = COALESCE(:3, PASSWORD_HASH),
                ID_ROL = COALESCE(:4, ID_ROL)
            WHERE ID_USUARIO = :5
        """
        cursor.execute(sql, (
            usuario.nombre,
            usuario.email,
            usuario.password_hash,
            usuario.id_rol,
            id_usuario
        ))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": f"¡Usuario con ID {id_usuario} actualizado exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM USUARIOS WHERE ID_USUARIO = :1"
        cursor.execute(sql, (id_usuario,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": f"¡Usuario con ID {id_usuario} eliminado exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    