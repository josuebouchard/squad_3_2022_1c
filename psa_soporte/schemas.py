from pydantic import BaseModel
from datetime import datetime
from typing import List


class Ticket(BaseModel):
    id: int
    title: str
    description: str
    clientId: int
    priority: str  # PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA
    severity: str  # S1, S2, S3, S4
    state: str  # ABIERTO, CERRADO, EN_PROGRESO
    creationDate: datetime
    lastUpdateDate: datetime
    deadline: datetime

    class Config:
        orm_mode = True


class TicketPost(BaseModel):
    title: str
    description: str
    clientId: int
    tasks: List[int]
    employees: List[int]
    priority: str  # PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA
    severity: str  # S1, S2, S3, S4
    deadline: datetime

    class Config:
        orm_mode = True


class TicketUpdate(BaseModel):
    title: str
    description: str
    clientId: int
    tasks: List[int]
    priority: str  # PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA
    severity: str  # S1, S2, S3, S4
    state: str  # ABIERTO, CERRADO, EN_PROGRESO
    deadline: datetime
    employees: List[int]

    class Config:
        orm_mode = True
