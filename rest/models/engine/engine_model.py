from pydantic import BaseModel, Field, constr, conint
from typing import List, Dict, Any


class engineSpecification_Log(BaseModel):
    level: str

class engineSpecification(BaseModel):
    jvmConfig: List[str]
    exposedPorts: List[Dict[Any, Any]]
    sharedNamespace: int
    log: engineSpecification_Log
    environmentVariables: List[str]

class engineSettings(BaseModel):
    settingAaa: Dict[Any, Any]
    settingAab: Dict[Any, Any]


class Configuration(BaseModel):
    specification: engineSpecification
    settings: engineSettings

class EngineDocument(BaseModel):
    kind: constr(max_length=32) = Field(default="engine", const=True)
    name: constr(max_length=128)
    version: constr(regex=r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
    description: constr(max_length=4096)
    configuration: Configuration