from sqlmodel import select

from model import (
    PacienteID, PacienteBase, PacienteUpdate,
    DoctorID, DoctorBase, DoctorUpdate,
    CitaID, CitaBase, CitaUpdate
)
from enums import EstadoRegistro


# =====================
# PACIENTES
# =====================

def create_paciente_db(paciente: PacienteBase, session):
    db_paciente = PacienteID.model_validate(paciente)
    session.add(db_paciente)
    session.commit()
    session.refresh(db_paciente)
    return db_paciente


def find_one_paciente_db(id: int, session):
    return session.get(PacienteID, id)


def all_pacientes_db(session, offset: int = 0, limit: int = 20):
    statement = select(PacienteID).offset(offset).limit(limit)
    return session.exec(statement).all()


def updated_paciente_db(id: int, paciente_update: PacienteUpdate, session):
    paciente = session.get(PacienteID, id)

    if not paciente:
        return None

    paciente_data = paciente_update.model_dump(exclude_unset=True)

    for key, value in paciente_data.items():
        setattr(paciente, key, value)

    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    return paciente


def soft_delete_paciente_db(id: int, session):
    paciente = session.get(PacienteID, id)

    if not paciente:
        return None

    paciente.estado = EstadoRegistro.INACTIVO

    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    return paciente


def search_pacientes_by_nombre(nombre: str, session, offset: int = 0, limit: int = 20):
    statement = (
        select(PacienteID)
        .where(PacienteID.nombre.ilike(f"%{nombre}%"))
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


def filter_pacientes(estado, session, offset: int = 0, limit: int = 20):
    statement = select(PacienteID)

    if estado:
        statement = statement.where(PacienteID.estado == estado)

    statement = statement.offset(offset).limit(limit)

    return session.exec(statement).all()


# =====================
# DOCTORES
# =====================

def create_doctor_db(doctor: DoctorBase, session):
    db_doctor = DoctorID.model_validate(doctor)
    session.add(db_doctor)
    session.commit()
    session.refresh(db_doctor)
    return db_doctor


def find_one_doctor_db(id: int, session):
    return session.get(DoctorID, id)


def all_doctores_db(session, offset: int = 0, limit: int = 20):
    statement = select(DoctorID).offset(offset).limit(limit)
    return session.exec(statement).all()


def updated_doctor_db(id: int, doctor_update: DoctorUpdate, session):
    doctor = session.get(DoctorID, id)

    if not doctor:
        return None

    doctor_data = doctor_update.model_dump(exclude_unset=True)

    for key, value in doctor_data.items():
        setattr(doctor, key, value)

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return doctor


def soft_delete_doctor_db(id: int, session):
    doctor = session.get(DoctorID, id)

    if not doctor:
        return None

    doctor.estado = EstadoRegistro.INACTIVO

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return doctor


def search_doctores_by_especialidad(especialidad: str, session, offset: int = 0, limit: int = 20):
    statement = (
        select(DoctorID)
        .where(DoctorID.especialidad.ilike(f"%{especialidad}%"))
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


def filter_doctores(estado, consultorio, session, offset: int = 0, limit: int = 20):
    statement = select(DoctorID)

    if estado:
        statement = statement.where(DoctorID.estado == estado)

    if consultorio:
        statement = statement.where(DoctorID.consultorio == consultorio)

    statement = statement.offset(offset).limit(limit)

    return session.exec(statement).all()


# =====================
# CITAS
# =====================

def create_cita_db(cita: CitaBase, session):
    db_cita = CitaID.model_validate(cita)
    session.add(db_cita)
    session.commit()
    session.refresh(db_cita)
    return db_cita


def find_one_cita_db(id: int, session):
    return session.get(CitaID, id)


def all_citas_db(session, offset: int = 0, limit: int = 20):
    statement = select(CitaID).offset(offset).limit(limit)
    return session.exec(statement).all()


def updated_cita_db(id: int, cita_update: CitaUpdate, session):
    cita = session.get(CitaID, id)

    if not cita:
        return None

    cita_data = cita_update.model_dump(exclude_unset=True)

    for key, value in cita_data.items():
        setattr(cita, key, value)

    session.add(cita)
    session.commit()
    session.refresh(cita)

    return cita


def soft_delete_cita_db(id: int, session):
    cita = session.get(CitaID, id)

    if not cita:
        return None

    cita.estado = EstadoRegistro.INACTIVO

    session.add(cita)
    session.commit()
    session.refresh(cita)

    return cita


def search_citas_by_fecha(fecha: str, session, offset: int = 0, limit: int = 20):
    statement = (
        select(CitaID)
        .where(CitaID.fecha == fecha)
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


def filter_citas(
    fecha,
    doctor_id,
    paciente_id,
    estado,
    session,
    offset: int = 0,
    limit: int = 20
):
    statement = select(CitaID)

    if fecha:
        statement = statement.where(CitaID.fecha == fecha)

    if doctor_id:
        statement = statement.where(CitaID.doctor_id == doctor_id)

    if paciente_id:
        statement = statement.where(CitaID.paciente_id == paciente_id)

    if estado:
        statement = statement.where(CitaID.estado == estado)

    statement = statement.offset(offset).limit(limit)

    return session.exec(statement).all()