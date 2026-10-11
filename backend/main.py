from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import get_db_connection
from routers import equipos_router

app = FastAPI(
    title="API Automatización de Producción",
    description="Backend FastAPI + Oracle para el Proyecto Integrador",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensaje": "¡La API de Automatización está funcionando perfectamente!"}

@app.get("/api/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP FROM DUAL")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"estado": "Conexión exitosa a Oracle", "tiempo": str(row[0])}
    except Exception as e:
        return {"estado": "Error de conexión", "detalles": str(e)}

    from routers import equipos_router

from fastapi import FastAPI
from routers import equipos_router, usuarios_router  # <--- Importar el nuevo router

app = FastAPI(title="API Automatización Industrial", version="1.0")

# Incluir las rutas
app.include_router(equipos_router.router)
app.include_router(usuarios_router.router)  # <--- Registrar el router de usuarios

@app.get("/")
def root():
    return {"mensaje": "¡API funcionando correctamente conectada a Oracle FreeSQL!"}

from fastapi import FastAPI
from routers import equipos_router, usuarios_router, ordenes_router  # <--- Incluir ordenes_router

app = FastAPI(title="API Automatización Industrial", version="1.0")

app.include_router(equipos_router.router)
app.include_router(usuarios_router.router)
app.include_router(ordenes_router.router)  # <--- Registrar el router de órdenes

@app.get("/")
def root():
    return {"mensaje": "¡API funcionando correctamente conectada a Oracle FreeSQL!"}
