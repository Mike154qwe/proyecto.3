import random

import pandas as pd
from sqlmodel import Session, SQLModel, select

from db import engine
from model import PacienteID, DoctorID, CitaID
from enums import EstadoRegistro, TipoConsulta


CSV_PATH = "dataset/archive/KaggleV2-May-2016.csv"

ESPECIALIDADES = [
    "Medicina General",
    "Odontologia",
    "Pediatria",
    "Medicina Interna",
    "Dermatologia",
]

TIPOS_CONSULTA = [
    TipoConsulta.GENERAL,
    TipoConsulta.ODONTOLOGIA,
    TipoConsulta.PEDIATRIA,
    TipoConsulta.MEDICINA_INTERNA,
    TipoConsulta.DERMATOLOGIA,
]


def cargar_doctores(session):
    doctores = []

    for i, especialidad in enumerate(ESPECIALIDADES, start=1):
        doctor = DoctorID(
            nombre=f"Doctor {especialidad}",
            especialidad=especialidad,
            consultorio=str(i),
            imagen_url=f"https://placehold.co/300x200?text={especialidad.replace(' ', '+')}",
            estado=EstadoRegistro.ACTIVO,
        )

        session.add(doctor)
        doctores.append(doctor)

    session.commit()

    for doctor in doctores:
        session.refresh(doctor)

    return doctores


def cargar_dataset():
    print("Creando tablas...")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        # Evitar duplicados al reiniciar Render
        existe_cita = session.exec(
            select(CitaID)
        ).first()

        if existe_cita:
            print("Dataset ya cargado. No se duplican datos.")
            return

        print("Leyendo dataset...")

        df = pd.read_csv(CSV_PATH)
        df = df.head(300)

        doctores = cargar_doctores(session)

        pacientes_creados = {}

        for _, row in df.iterrows():

            patient_id = int(row["PatientId"])

            if patient_id not in pacientes_creados:

                paciente = PacienteID(
                    nombre=f"Paciente {patient_id}",
                    documento=str(patient_id),
                    telefono="3000000000",
                    estado=EstadoRegistro.ACTIVO,
                )

                session.add(paciente)
                session.commit()
                session.refresh(paciente)

                pacientes_creados[patient_id] = paciente

            doctor = random.choice(doctores)

            cita = CitaID(
                paciente_id=pacientes_creados[patient_id].id,
                doctor_id=doctor.id,
                tipo_consulta=random.choice(TIPOS_CONSULTA),
                fecha=str(row["AppointmentDay"])[:10],
                hora=f"{random.randint(7,16)}:00",
                estado=EstadoRegistro.ACTIVO,
            )

            session.add(cita)

        session.commit()

    print("================================")
    print("Dataset cargado correctamente")
    print(f"Pacientes creados: {len(pacientes_creados)}")
    print(f"Doctores creados: {len(doctores)}")
    print(f"Citas creadas: {len(df)}")
    print("================================")


if __name__ == "__main__":
    cargar_dataset()