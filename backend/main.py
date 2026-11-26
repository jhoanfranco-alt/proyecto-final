from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Fragancia Selecta")

# Configurar CORS para permitir que tu frontend (HTML/JS) consuma esta API sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes cambiar "*" por tu dominio
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos de un Perfume
class Perfume(BaseModel):
    id: Optional[int] = None
    src: str
    nombre: str
    marca: str = "Sin marca"
    familia_olfativa: str
    mililitros: int = 100
    precio: float
    stock: int = 10

# Lista en memoria con perfumes iniciales de ejemplo
catalogo_perfumes: List[Perfume] = [
    Perfume(id=1, src="assets/SORBETTO_ROSSO.jpeg", nombre="SORBETTO ROSSO", familia_olfativa="Acuatico, afrutado y dulce",  precio=80000, stock=15),
    Perfume(id=2, src="assets/BOMBSHELL.jpeg", nombre="BOMBSHELL",  familia_olfativa="Afrutado, dulce y fresco",  precio=80000, stock=8),
    Perfume(id=3, src="assets/THANK_YOU_NEXT_2.0.jpeg", nombre="THANK YOU NEXT 2.0 ",  familia_olfativa="Afrutado, dulce y atalcado", precio=90000, stock=12),
    Perfume(id=4, src="assets/CLOUD_2.0_INTENSE.jpeg", nombre="CLOUD 2.0 INTENSE",  familia_olfativa="amaderado, dulce y al0mizclado", precio=470000, stock=20),
    Perfume(id=5, src="assets/CLOUD.jpeg", nombre="CLOUD",  familia_olfativa="avainillado, dulce y coco", precio=90000, stock=5),
    Perfume(id=6, src="assets/REM.jpeg", nombre="REM",  familia_olfativa="atalcado, caramelo y dulce", precio=90000, stock=10),
]

# --- 1. LISTAR TODOS LOS PERFUMES (O FILTRAR POR BÚSQUEDA) ---
@app.get("/perfumes/", response_model=List[Perfume])
def listar_perfumes(buscar: Optional[str] = None):
    if buscar:
        termino = buscar.lower()
        return [
            p for p in catalogo_perfumes
            if termino in p.nombre.lower() or termino in p.marca.lower() or termino in p.familia_olfativa.lower()
        ]
    return catalogo_perfumes

# --- 2. OBTENER UN PERFUME POR ID ---
@app.get("/perfumes/{perfume_id}", response_model=Perfume)
def obtener_perfume(perfume_id: int):
    for perfume in catalogo_perfumes:
        if perfume.id == perfume_id:
            return perfume
    raise HTTPException(status_code=404, detail="Perfume no encontrado")

# --- 3. AGREGAR UN NUEVO PERFUME A LA LISTA ---
@app.post("/perfumes/", response_model=Perfume, status_code=201)
def agregar_perfume(perfume: Perfume):
    nuevo_id = max([p.id for p in catalogo_perfumes], default=0) + 1
    perfume.id = nuevo_id
    catalogo_perfumes.append(perfume)
    return perfume

# --- 4. ELIMINAR UN PERFUME DE LA LISTA ---
@app.delete("/perfumes/{perfume_id}")
def eliminar_perfume(perfume_id: int):
    for index, perfume in enumerate(catalogo_perfumes):
        if perfume.id == perfume_id:
            catalogo_perfumes.pop(index)
            return {"mensaje": f"Perfume '{perfume.nombre}' eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Perfume no encontrado")