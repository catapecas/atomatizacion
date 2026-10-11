from pydantic import BaseModel
from typing import Optional

class EquipoCreate(BaseModel):
    nombre_equipo: str
    tipo: str
    estado: str
    ubicacion: Optional[str] = None

class EquipoResponse(EquipoCreate):
    id_equipo: int

    class Config:
        from_attributes = True