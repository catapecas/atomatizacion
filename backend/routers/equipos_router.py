from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database.connection import get_db_connection

router = APIRouter(prefix="/api/equipos", tags=["Equipos de Automatización"])

class EquipoCreate(BaseModel):
    codigo_activo: str
    nombre_equipo: str
    tipo: str
    ubicacion_planta: str
    estado: Optional[str] = "Operativo"

class EquipoUpdate(BaseModel):
    codigo_activo: Optional[str] = None
    nombre_equipo: Optional[str] = None
    tipo: Optional[str] = None
    ubicacion_planta: Optional[str] = None
    estado: Optional[str] = None

@router.get("/")
def listar_equipos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID_EQUIPO, CODIGO_ACTIVO, NOMBRE_EQUIPO, TIPO, UBICACION_PLANTA, ESTADO 
            FROM EQUIPOS_AUTOMATIZACION
        """)
        rows = cursor.fetchall()
        
        equipos = []
        for row in rows:
            equipos.append({
                "id_equipo": row[0],
                "codigo_activo": row[1],
                "nombre_equipo": row[2],
                "tipo": row[3],
                "ubicacion_planta": row[4],
                "estado": row[5]
            })
            
        cursor.close()
        conn.close()
        return equipos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_equipo(equipo: EquipoCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO EQUIPOS_AUTOMATIZACION (CODIGO_ACTIVO, NOMBRE_EQUIPO, TIPO, UBICACION_PLANTA, ESTADO)
            VALUES (:1, :2, :3, :4, :5)
        """
        cursor.execute(sql, (
            equipo.codigo_activo, 
            equipo.nombre_equipo, 
            equipo.tipo, 
            equipo.ubicacion_planta, 
            equipo.estado
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "¡Equipo creado exitosamente!", "equipo": equipo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_equipo}")
def actualizar_equipo(id_equipo: int, equipo: EquipoUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE EQUIPOS_AUTOMATIZACION 
            SET CODIGO_ACTIVO = COALESCE(:1, CODIGO_ACTIVO),
                NOMBRE_EQUIPO = COALESCE(:2, NOMBRE_EQUIPO),
                TIPO = COALESCE(:3, TIPO),
                UBICACION_PLANTA = COALESCE(:4, UBICACION_PLANTA),
                ESTADO = COALESCE(:5, ESTADO)
            WHERE ID_EQUIPO = :6
        """
        cursor.execute(sql, (
            equipo.codigo_activo,
            equipo.nombre_equipo,
            equipo.tipo,
            equipo.ubicacion_planta,
            equipo.estado,
            id_equipo
        ))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": f"¡Equipo con ID {id_equipo} actualizado exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_equipo}")
def eliminar_equipo(id_equipo: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM EQUIPOS_AUTOMATIZACION WHERE ID_EQUIPO = :1"
        cursor.execute(sql, (id_equipo,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": f"¡Equipo con ID {id_equipo} eliminado exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    