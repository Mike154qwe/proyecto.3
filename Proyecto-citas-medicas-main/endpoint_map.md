# Mapa de Endpoints

## Pacientes
- `POST /pacientes` -> crear paciente
- `GET /pacientes` -> listar pacientes
- `GET /pacientes/{id}` -> obtener paciente por ID
- `PATCH /pacientes/{id}` -> actualizar paciente
- `DELETE /pacientes/{id}` -> inactivar paciente (historico)
- `GET /pacientes/buscar/?nombre=Juan` -> buscar por nombre
- `GET /pacientes/filtrar/?estado=ACTIVO` -> filtrar por estado

## Doctores
- `POST /doctores` -> crear doctor
- `GET /doctores` -> listar doctores
- `GET /doctores/{id}` -> obtener doctor por ID
- `PATCH /doctores/{id}` -> actualizar doctor
- `DELETE /doctores/{id}` -> inactivar doctor (historico)
- `GET /doctores/buscar/?especialidad=ODONTO` -> buscar por especialidad
- `GET /doctores/filtrar/?estado=ACTIVO&consultorio=101` -> filtrar por estado y consultorio

## Citas
- `POST /citas` -> crear cita
- `GET /citas` -> listar citas
- `GET /citas/{id}` -> obtener cita por ID
- `PATCH /citas/{id}` -> actualizar cita
- `DELETE /citas/{id}` -> inactivar cita (historico)
- `GET /citas/buscar/?fecha=2026-04-25` -> buscar por fecha
- `GET /citas/filtrar/?fecha=2026-04-25&doctor_id=1&estado=ACTIVO` -> filtrar citas
