from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database.connection import get_db_connection

router = APIRouter(prefix="/api/ordenes", tags=["Órdenes de Trabajo"])

class OrdenCreate(BaseModel):
    id_equipo: int
    id_usuario_solicitante: int
    descripcion_falla: str
    prioridad: str
    estado_ot: Optional[str] = "Pendiente"

class OrdenUpdate(BaseModel):
    id_equipo: Optional[int] = None
    id_usuario_solicitante: Optional[int] = None
    descripcion_falla: Optional[str] = None
    prioridad: Optional[str] = None
    estado_ot: Optional[str] = None

@router.get("/")
def listar_ordenes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID_OT, ID_EQUIPO, ID_USUARIO_SOLICITANTE, DESCRIPCION_FALLA, PRIORIDAD, ESTADO_OT 
            FROM ORDENES_TRABAJO
        """)
        rows = cursor.fetchall()
        
        ordenes = []
        for row in rows:
            ordenes.append({
                "id_ot": row[0],
                "id_equipo": row[1],
                "id_usuario_solicitante": row[2],
                "descripcion_falla": row[3],
                "prioridad": row[4],
                "estado_ot": row[5]
            })
            
        cursor.close()
        conn.close()
        return ordenes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_orden(orden: OrdenCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO ORDENES_TRABAJO (ID_EQUIPO, ID_USUARIO_SOLICITANTE, DESCRIPCION_FALLA, PRIORIDAD, ESTADO_OT)
            VALUES (:1, :2, :3, :4, :5)
        """
        cursor.execute(sql, (
            orden.id_equipo, 
            orden.id_usuario_solicitante, 
            orden.descripcion_falla, 
            orden.prioridad, 
            orden.estado_ot
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "¡Orden de trabajo creada exitosamente!", "orden": orden}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_ot}")
def actualizar_orden(id_ot: int, orden: OrdenUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE ORDENES_TRABAJO 
            SET ID_EQUIPO = COALESCE(:1, ID_EQUIPO),
                ID_USUARIO_SOLICITANTE = COALESCE(:2, ID_USUARIO_SOLICITANTE),
                DESCRIPCION_FALLA = COALESCE(:3, DESCRIPCION_FALLA),
                PRIORIDAD = COALESCE(:4, PRIORIDAD),
                ESTADO_OT = COALESCE(:5, ESTADO_OT)
            WHERE ID_OT = :6
        """
        cursor.execute(sql, (
            orden.id_equipo,
            orden.id_usuario_solicitante,
            orden.descripcion_falla,
            orden.prioridad,
            orden.estado_ot,
            id_ot
        ))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": f"¡Orden de trabajo con ID {id_ot} actualizada exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_ot}")
def eliminar_orden(id_ot: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM ORDENES_TRABAJO WHERE ID_OT = :1"
        cursor.execute(sql, (id_ot,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": f"¡Orden de trabajo con ID {id_ot} eliminada exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    