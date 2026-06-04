from enum import Enum


class EstadoRegistro(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class TipoConsulta(str, Enum):
    GENERAL = "GENERAL"
    ODONTOLOGIA = "ODONTOLOGIA"
    PEDIATRIA = "PEDIATRIA"
    MEDICINA_INTERNA = "MEDICINA_INTERNA"
    DERMATOLOGIA = "DERMATOLOGIA"
