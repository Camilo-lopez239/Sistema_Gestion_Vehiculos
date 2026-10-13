from fastapi import FastAPI, HTTPException, status
from pydantic import  BaseModel
from typing import List, Optional 

app = FastAPI(
    title="API Biblioteca pública - ADSO",
    description="API RESTfull completa con operaciones CRUD para auditoria de servicios web",
    version="2.0.0"
)

class Vehiculo(BaseModel):
    id: int
    placa: str
    marca_modelo: str 
    kilometraje: int
    orden_trabajo_activa: bool = True

class VehiculoUpdate(BaseModel):
    placa: str
    marca_modelo: str 
    kilometraje: int
    orden_trabajo_activa: bool

db_vehiculos: List[Vehiculo] =[
    Vehiculo(id=1, placa="ABC123" ,marca_modelo="Mazda 3",kilometraje=5000,orden_trabajo_activa=True),
    Vehiculo(id=2, placa="XYZ7879" ,marca_modelo="Chevriket Onix",kilometraje=20000,orden_trabajo_activa=False)
]

@app.get("/api/v1/vehiculos", response_model=List[Vehiculo], status_code=status.HTTP_200_OK)
def obtener_todos_los_vehiculos():
    return db_vehiculos

@app.get("/api/v1/vehiculos/{vehiculo_id}", response_model=Vehiculo, status_code=status.HTTP_200_OK)
def obtener_vehiculo_por_id(vehiculo_id: int):
    for vehiculo in db_vehiculos:
        if vehiculo.id == vehiculo_id:
            return vehiculo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El vehiculo con ID {vehiculo_id} no existe en el sistema del taller."
    )

@app.post("/api/v1/vehiculos", response_model=Vehiculo, status_code=status.HTTP_201_CREATED)
def crear_nuevo_vehiculo(vehiculo: Vehiculo):
    for v in db_vehiculos:
        if v.id == vehiculo.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de registro: ya existe un vehiculo con el ID {vehiculo.id}"
            )
    db_vehiculos.append(vehiculo)
    return vehiculo

@app.put("/api/v1/vehiculos/{vehiculo_id}", response_model=Vehiculo, status_code=status.HTTP_200_OK)
def actualizar_vehiculo(vehiculo_id: int, datos_actualizados: VehiculoUpdate):
    for index, vehiculo in enumerate(db_vehiculos):
        if vehiculo.id == vehiculo_id:
            vehiculo_modificado = Vehiculo(
                id=vehiculo_id,
                placa=datos_actualizados.placa,
                marca_modelo=datos_actualizados.marca_modelo,
                kilometraje=datos_actualizados.kilometraje,
                orden_trabajo_activa=datos_actualizados.orden_trabajo_activa
            )
            db_vehiculos[index] = vehiculo_modificado
            return vehiculo_modificado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actuaizar. El vehiculo con ID {vehiculo_id} no fue encontrado"
    )

@app.delete("/api/v1/vehiculos/{vehiculo_id}", status_code=status.HTTP_200_OK)
def eliminar_vehiculo(vehiculo_id: int):
    for index, vehiculo in enumerate(db_vehiculos):
        if vehiculo.id == vehiculo_id:
            db_vehiculos.pop(index)
            return {"mensaje": f"El vehiculo con ID {vehiculo_id} fue eliminado exitosamente"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El vehiculo con ID {vehiculo_id} no existe-"
    )