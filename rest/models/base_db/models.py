import enum
import uuid

from sqlalchemy import Column, String, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from rest.database import Base


class AppState(enum.Enum):
    NEW = "NEW"
    INSTALLING = "INSTALLING"
    RUNNING = "RUNNING"

class JSON_App(Base):
    __tablename__ = "apps"

    UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kind = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    version = Column(String(32), nullable=False)
    description = Column(String(4096))
    state = Column(Enum(AppState, name="state"), default=AppState.NEW, nullable=False)
    json = Column(JSON)