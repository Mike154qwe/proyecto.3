from datetime import date
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from model import (
    PacienteBase, PacienteID, PacienteUpdate,
    DoctorBase, DoctorID, DoctorUpdate,
    CitaBase, CitaID, CitaUpdate
)
from enums import EstadoRegistro


# =====================
# PACIENTES
# =====================
def create_paciente_db(paciente: PacienteBase, session: Session):
    if paciente.documento:
        statement = select(PacienteID).where(PacienteID.documento == paciente.documento)
        if session.exec(statement).first():
            raise ValueError("Ya existe un paciente con ese documento")

    new = PacienteID.model_validate(paciente)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new


def find_one_paciente_db(paciente_id: int, session: Session):
    try:
        return session.get_one(PacienteID, paciente_id)
    except NoResultFound:
        return None


def all_pacientes_db(session: Session):
    return session.exec(select(PacienteID)).all()


def updated_paciente_db(paciente_id: int, new_paciente: PacienteUpdate, session: Session):
    paciente = find_one_paciente_db(paciente_id, session)
    if paciente is None:
        return None

    update_data = new_paciente.model_dump(exclude_unset=True)

    if "documento" in update_data and update_data["documento"] != paciente.documento:
        statement = select(PacienteID).where(PacienteID.documento == update_data["documento"])
        exists = session.exec(statement).first()
        if exists:
            raise ValueError("Ya existe un paciente con ese documento")

    paciente.sqlmodel_update(update_data)
    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


def soft_delete_paciente_db(paciente_id: int, session: Session):
    paciente = find_one_paciente_db(paciente_id, session)
    if paciente is None:
        return None

    cita_activa = session.exec(
        select(CitaID).where(
            CitaID.paciente_id == paciente_id,
            CitaID.estado == EstadoRegistro.ACTIVO
        )
    ).first()

    if cita_activa:
        raise ValueError("No se puede inactivar el paciente porque tiene citas activas")

    paciente.estado = EstadoRegistro.INACTIVO
    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


def search_pacientes_by_nombre(nombre: str, session: Session):
    statement = select(PacienteID).where(PacienteID.nombre.contains(nombre))
    return session.exec(statement).all()


def filter_pacientes(estado: str | None, session: Session):
    statement = select(PacienteID)

    if estado:
        statement = statement.where(PacienteID.estado == estado)

    return session.exec(statement).all()


# =====================
# DOCTORES
# =====================
def create_doctor_db(doctor: DoctorBase, session: Session):
    new = DoctorID.model_validate(doctor)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new


def find_one_doctor_db(doctor_id: int, session: Session):
    try:
        return session.get_one(DoctorID, doctor_id)
    except NoResultFound:
        return None


def all_doctores_db(session: Session):
    return session.exec(select(DoctorID)).all()


def updated_doctor_db(doctor_id: int, new_doctor: DoctorUpdate, session: Session):
    doctor = find_one_doctor_db(doctor_id, session)
    if doctor is None:
        return None

    update_data = new_doctor.model_dump(exclude_unset=True)
    doctor.sqlmodel_update(update_data)

    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


def soft_delete_doctor_db(doctor_id: int, session: Session):
    doctor = find_one_doctor_db(doctor_id, session)
    if doctor is None:
        return None

    cita_activa = session.exec(
        select(CitaID).where(
            CitaID.doctor_id == doctor_id,
            CitaID.estado == EstadoRegistro.ACTIVO
        )
    ).first()

    if cita_activa:
        raise ValueError("No se puede inactivar el doctor porque tiene citas activas")

    doctor.estado = EstadoRegistro.INACTIVO
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


def search_doctores_by_especialidad(especialidad: str, session: Session):
    statement = select(DoctorID).where(DoctorID.especialidad.contains(especialidad))
    return session.exec(statement).all()


def filter_doctores(estado: str | None, consultorio: str | None, session: Session):
    statement = select(DoctorID)

    if estado:
        statement = statement.where(DoctorID.estado == estado)

    if consultorio:
        statement = statement.where(DoctorID.consultorio == consultorio)

    return session.exec(statement).all()


# =====================
# CITAS
# =====================
def create_cita_db(cita: CitaBase, session: Session):
    paciente = find_one_paciente_db(cita.paciente_id, session)
    if paciente is None or paciente.estado != EstadoRegistro.ACTIVO:
        raise ValueError("El paciente no existe o esta inactivo")

    doctor = find_one_doctor_db(cita.doctor_id, session)
    if doctor is None or doctor.estado != EstadoRegistro.ACTIVO:
        raise ValueError("El doctor no existe o esta inactivo")

    if cita.fecha < date.today().isoformat():
        raise ValueError("No se puede crear una cita en una fecha pasada")

    conflicto = session.exec(
        select(CitaID).where(
            CitaID.doctor_id == cita.doctor_id,
            CitaID.fecha == cita.fecha,
            CitaID.hora == cita.hora,
            CitaID.estado == EstadoRegistro.ACTIVO
        )
    ).first()

    if conflicto:
        raise ValueError("El doctor ya tiene una cita activa en esa fecha y hora")

    new = CitaID.model_validate(cita)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new


def find_one_cita_db(cita_id: int, session: Session):
    try:
        return session.get_one(CitaID, cita_id)
    except NoResultFound:
        return None


def all_citas_db(session: Session):
    return session.exec(select(CitaID)).all()


def updated_cita_db(cita_id: int, new_cita: CitaUpdate, session: Session):
    cita = find_one_cita_db(cita_id, session)
    if cita is None:
        return None

    update_data = new_cita.model_dump(exclude_unset=True)

    paciente_id = update_data.get("paciente_id", cita.paciente_id)
    doctor_id = update_data.get("doctor_id", cita.doctor_id)
    fecha = update_data.get("fecha", cita.fecha)
    hora = update_data.get("hora", cita.hora)

    paciente = find_one_paciente_db(paciente_id, session)
    if paciente is None or paciente.estado != EstadoRegistro.ACTIVO:
        raise ValueError("El paciente no existe o esta inactivo")

    doctor = find_one_doctor_db(doctor_id, session)
    if doctor is None or doctor.estado != EstadoRegistro.ACTIVO:
        raise ValueError("El doctor no existe o esta inactivo")

    if fecha < date.today().isoformat():
        raise ValueError("No se puede actualizar una cita a una fecha pasada")

    conflicto = session.exec(
        select(CitaID).where(
            CitaID.id != cita_id,
            CitaID.doctor_id == doctor_id,
            CitaID.fecha == fecha,
            CitaID.hora == hora,
            CitaID.estado == EstadoRegistro.ACTIVO
        )
    ).first()

    if conflicto:
        raise ValueError("El doctor ya tiene otra cita activa en esa fecha y hora")

    cita.sqlmodel_update(update_data)
    session.add(cita)
    session.commit()
    session.refresh(cita)
    return cita


def soft_delete_cita_db(cita_id: int, session: Session):
    cita = find_one_cita_db(cita_id, session)
    if cita is None:
        return None

    cita.estado = EstadoRegistro.INACTIVO
    session.add(cita)
    session.commit()
    session.refresh(cita)
    return cita


def search_citas_by_fecha(fecha: str, session: Session):
    statement = select(CitaID).where(CitaID.fecha == fecha)
    return session.exec(statement).all()


def filter_citas(
    fecha: str | None,
    doctor_id: int | None,
    paciente_id: int | None,
    estado: str | None,
    session: Session
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

    return session.exec(statement).all()