from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Ticket(BaseModel):
    id: int
    title: str
    description: str
    clientId: int
    versionId: int
    priority: str  # PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA
    severity: str  # S1, S2, S3, S4
    state: str  # ABIERTO, CERRADO, EN_PROGRESO
    creationDate: datetime
    lastUpdateDate: datetime
    deadline: datetime
    employees: list
    tasks: list

    class Config:
        orm_mode = True


class TicketPost(BaseModel):
    title: str
    description: str
    clientId: int
    versionId: int
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
    priority: str  # PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA
    severity: str  # S1, S2, S3, S4
    state: str  # ABIERTO, CERRADO, EN_PROGRESO
    deadline: datetime
    tasks: Optional[List[int]]
    employees: Optional[List[int]]

    class Config:
        orm_mode = True
