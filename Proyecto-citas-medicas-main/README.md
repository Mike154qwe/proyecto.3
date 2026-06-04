# Proyecto: Sistema de Gestion de Citas Medicas

Este proyecto fue construido para cumplir los criterios de aceptacion del ejercicio

- Presenta 3 modelos de datos reales:
  - Paciente
  - Doctor
  - Cita
- Cada modelo cuenta con operaciones CRUD
- La eliminacion es logica usando campo `estado`, lo que permite historico
- Tiene endpoints de filtro
- Tiene busqueda por atributos diferentes al ID
- Incluye manejo de excepciones
- Incluye mapa de endpoints

## Reglas de negocio implementadas
- No se puede crear una cita con paciente inactivo o inexistente
- No se puede crear una cita con doctor inactivo o inexistente
- No se puede asignar al mismo doctor dos citas activas en la misma fecha y hora
- No se puede inactivar un paciente si tiene citas activas
- No se puede inactivar un doctor si tiene citas activas

## Archivos principales
- `main.py`
- `db.py`
- `model.py`
- `enums.py`
- `operation_db.py`
- `endpoint_map.md`
- `test_main.http`

## Configuracion
1. Crea un archivo `.env`
2. Copia el contenido de `.env.example`
3. Si no tienes Neon, puedes usar SQLite local con el valor por defecto

## Instalacion
```bash
pip install -r requirements.txt
```

## Ejecucion
```bash
python -m uvicorn main:app --reload
```

## Documentacion
Abre:
`http://127.0.0.1:8000/docs`
