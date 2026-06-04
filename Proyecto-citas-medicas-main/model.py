from sqlmodel import SQLModel, Field
from enums import EstadoRegistro, TipoConsulta


class PacienteBase(SQLModel):
    nombre: str | None = Field(default=None, min_length=4, max_length=80)
    documento: str | None = Field(default=None, min_length=5, max_length=20)
    telefono: str | None = Field(default=None, min_length=7, max_length=20)
    estado: EstadoRegistro | None = Field(default=EstadoRegistro.ACTIVO)


class PacienteID(PacienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PacienteUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=4, max_length=80)
    documento: str | None = Field(default=None, min_length=5, max_length=20)
    telefono: str | None = Field(default=None, min_length=7, max_length=20)
    estado: EstadoRegistro | None = Field(default=None)


class DoctorBase(SQLModel):
    nombre: str | None = Field(default=None, min_length=4, max_length=80)
    especialidad: str | None = Field(default=None, min_length=4, max_length=60)
    consultorio: str | None = Field(default=None, min_length=1, max_length=20)
    imagen_url: str | None = Field(default=None, max_length=300)
    estado: EstadoRegistro | None = Field(default=EstadoRegistro.ACTIVO)


class DoctorID(DoctorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class DoctorUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=4, max_length=80)
    especialidad: str | None = Field(default=None, min_length=4, max_length=60)
    consultorio: str | None = Field(default=None, min_length=1, max_length=20)
    imagen_url: str | None = Field(default=None, max_length=300)
    estado: EstadoRegistro | None = Field(default=None)


class CitaBase(SQLModel):
    paciente_id: int | None = Field(default=None, gt=0)
    doctor_id: int | None = Field(default=None, gt=0)
    tipo_consulta: TipoConsulta | None = Field(default=TipoConsulta.GENERAL)
    fecha: str | None = Field(default=None)
    hora: str | None = Field(default=None)
    estado: EstadoRegistro | None = Field(default=EstadoRegistro.ACTIVO)


class CitaID(CitaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CitaUpdate(SQLModel):
    paciente_id: int | None = Field(default=None, gt=0)
    doctor_id: int | None = Field(default=None, gt=0)
    tipo_consulta: TipoConsulta | None = Field(default=None)
    fecha: str | None = Field(default=None)
    hora: str | None = Field(default=None)
    estado: EstadoRegistro | None = Field(default=None)