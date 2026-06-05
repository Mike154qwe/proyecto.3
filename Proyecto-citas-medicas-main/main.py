import os
import shutil

from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, HTTPException, Request, Query
from starlette.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from db import create_all_tables, SessionDep
from enums import EstadoRegistro
from model import (
    PacienteBase, PacienteID, PacienteUpdate,
    DoctorBase, DoctorID, DoctorUpdate,
    CitaBase, CitaID, CitaUpdate
)
from operation_db import (
    create_paciente_db, find_one_paciente_db, all_pacientes_db, updated_paciente_db, soft_delete_paciente_db,
    search_pacientes_by_nombre, filter_pacientes,
    create_doctor_db, find_one_doctor_db, all_doctores_db, updated_doctor_db, soft_delete_doctor_db,
    search_doctores_by_especialidad, filter_doctores,
    create_cita_db, find_one_cita_db, all_citas_db, updated_cita_db, soft_delete_cita_db,
    search_citas_by_fecha, filter_citas
)

app = FastAPI(
    title="Sistema de Gestion de Citas Medicas",
    version="2.0.0",
    lifespan=create_all_tables
)
os.makedirs("static/uploads", exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


templates = Jinja2Templates(directory="templates")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# =====================
# PACIENTES
# =====================
@app.post("/pacientes", response_model=PacienteID, status_code=201)
async def create_paciente(paciente: PacienteBase, session: SessionDep):
    return create_paciente_db(paciente, session)


@app.get("/pacientes", response_model=list[PacienteID])
async def get_pacientes(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=1, le=100)
):
    return all_pacientes_db(session, offset=offset, limit=limit)


@app.get("/pacientes/buscar/", response_model=list[PacienteID])
async def buscar_pacientes_por_nombre(
    nombre: str,
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=1, le=100)
):
    return search_pacientes_by_nombre(nombre, session, offset=offset, limit=limit)


@app.get("/pacientes/filtrar/", response_model=list[PacienteID])
async def filtrar_pacientes(
    session: SessionDep,
    estado: EstadoRegistro | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=1, le=100)
):
    return filter_pacientes(estado, session, offset=offset, limit=limit)


@app.get("/pacientes/{id}", response_model=PacienteID)
async def get_paciente(id: int, session: SessionDep):
    paciente = find_one_paciente_db(id, session)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@app.patch("/pacientes/{id}", response_model=PacienteID)
async def update_paciente(id: int, paciente_update: PacienteUpdate, session: SessionDep):
    updated = updated_paciente_db(id, paciente_update, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return updated


@app.delete("/pacientes/{id}", response_model=PacienteID)
async def delete_paciente(id: int, session: SessionDep):
    deleted = soft_delete_paciente_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return deleted


# =====================
# DOCTORES
# =====================
@app.post("/doctores", response_model=DoctorID, status_code=201)
async def create_doctor(doctor: DoctorBase, session: SessionDep):
    return create_doctor_db(doctor, session)


@app.get("/doctores", response_model=list[DoctorID])
async def get_doctores(session: SessionDep):
    return all_doctores_db(session)


@app.get("/doctores/buscar/", response_model=list[DoctorID])
async def buscar_doctores_por_especialidad(especialidad: str, session: SessionDep):
    return search_doctores_by_especialidad(especialidad, session)


@app.get("/doctores/filtrar/", response_model=list[DoctorID])
async def filtrar_doctores(
    session: SessionDep,
    estado: EstadoRegistro | None = Query(default=None),
    consultorio: str | None = Query(default=None)
):
    return filter_doctores(estado, consultorio, session)


@app.get("/doctores/{id}", response_model=DoctorID)
async def get_doctor(id: int, session: SessionDep):
    doctor = find_one_doctor_db(id, session)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return doctor


@app.patch("/doctores/{id}", response_model=DoctorID)
async def update_doctor(id: int, doctor_update: DoctorUpdate, session: SessionDep):
    updated = updated_doctor_db(id, doctor_update, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return updated


@app.delete("/doctores/{id}", response_model=DoctorID)
async def delete_doctor(id: int, session: SessionDep):
    deleted = soft_delete_doctor_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return deleted


# =====================
# CITAS
# =====================
@app.post("/citas", response_model=CitaID, status_code=201)
async def create_cita(cita: CitaBase, session: SessionDep):
    return create_cita_db(cita, session)


@app.get("/citas", response_model=list[CitaID])
async def get_citas(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100)
):
    return all_citas_db(session, offset=offset, limit=limit)


@app.get("/citas/buscar/", response_model=list[CitaID])
async def buscar_citas_por_fecha(fecha: str, session: SessionDep):
    return search_citas_by_fecha(fecha, session)


@app.get("/citas/filtrar/", response_model=list[CitaID])
async def filtrar_citas(
    session: SessionDep,
    fecha: str | None = Query(default=None),
    doctor_id: int | None = Query(default=None),
    paciente_id: int | None = Query(default=None),
    estado: EstadoRegistro | None = Query(default=None)
):
    return filter_citas(fecha, doctor_id, paciente_id, estado, session)


@app.get("/citas/{id}", response_model=CitaID)
async def get_cita(id: int, session: SessionDep):
    cita = find_one_cita_db(id, session)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


@app.patch("/citas/{id}", response_model=CitaID)
async def update_cita(id: int, cita_update: CitaUpdate, session: SessionDep):
    updated = updated_cita_db(id, cita_update, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return updated


@app.delete("/citas/{id}", response_model=CitaID)
async def delete_cita(id: int, session: SessionDep):
    deleted = soft_delete_cita_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return deleted


# =====================
# HALLAZGOS / DASHBOARD
# =====================
@app.get("/hallazgos/resumen")
async def hallazgos_resumen(session: SessionDep):
    pacientes = all_pacientes_db(session)
    doctores = all_doctores_db(session)
    citas = all_citas_db(session)

    return {
        "total_pacientes": len(pacientes),
        "total_doctores": len(doctores),
        "total_citas": len(citas),
        "mensaje": "Resumen general del sistema de citas medicas"
    }


@app.get("/hallazgos/especialidades")
async def hallazgos_especialidades(session: SessionDep):
    citas = all_citas_db(session)
    doctores = all_doctores_db(session)

    conteo = {}

    for cita in citas:
        doctor = next((d for d in doctores if d.id == cita.doctor_id), None)
        if doctor:
            especialidad = doctor.especialidad
            conteo[especialidad] = conteo.get(especialidad, 0) + 1

    return [
        {"especialidad": especialidad, "cantidad_citas": cantidad}
        for especialidad, cantidad in conteo.items()
    ]


@app.get("/hallazgos/pacientes-frecuentes")
async def hallazgos_pacientes_frecuentes(session: SessionDep):
    citas = all_citas_db(session)
    pacientes = all_pacientes_db(session)

    conteo = {}

    for cita in citas:
        conteo[cita.paciente_id] = conteo.get(cita.paciente_id, 0) + 1

    resultado = []

    for paciente_id, cantidad in conteo.items():
        paciente = next((p for p in pacientes if p.id == paciente_id), None)
        if paciente:
            resultado.append({
                "paciente_id": paciente.id,
                "paciente": paciente.nombre,
                "cantidad_citas": cantidad
            })

    return sorted(resultado, key=lambda x: x["cantidad_citas"], reverse=True)


@app.get("/hallazgos/doctores-top")
async def hallazgos_doctores_top(session: SessionDep):
    citas = all_citas_db(session)
    doctores = all_doctores_db(session)

    conteo = {}

    for cita in citas:
        conteo[cita.doctor_id] = conteo.get(cita.doctor_id, 0) + 1

    resultado = []

    for doctor_id, cantidad in conteo.items():
        doctor = next((d for d in doctores if d.id == doctor_id), None)
        if doctor:
            resultado.append({
                "doctor_id": doctor.id,
                "doctor": doctor.nombre,
                "especialidad": doctor.especialidad,
                "cantidad_citas": cantidad
            })

    return sorted(resultado, key=lambda x: x["cantidad_citas"], reverse=True)


@app.get("/hallazgos/tipos-consulta")
async def hallazgos_tipos_consulta(session: SessionDep):
    citas = all_citas_db(session)

    conteo = {}

    for cita in citas:
        tipo = str(cita.tipo_consulta)
        conteo[tipo] = conteo.get(tipo, 0) + 1

    return [
        {"tipo_consulta": tipo, "cantidad_citas": cantidad}
        for tipo, cantidad in conteo.items()
    ]


@app.post("/upload-imagen")
async def upload_imagen(file: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imagenes JPG, PNG o WEBP"
        )

    filename = file.filename.replace(" ", "_")
    file_path = f"static/uploads/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "imagen_url": f"/static/uploads/{filename}"
    }


    