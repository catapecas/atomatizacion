from pydantic import BaseModel
from typing import Optional

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
    