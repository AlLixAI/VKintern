from pydantic import BaseModel, Field, constr, conint
from typing import List, Dict, Any


class testSpecification_Log(BaseModel):
    level: str

class testSpecification(BaseModel):
    jvmConfig: List[str]
    exposedPorts: List[Dict[Any, Any]]
    sharedNamespace: int
    log: testSpecification_Log
    environmentVariables: List[str]

class testSettings(BaseModel):
    settingAaa: Dict[Any, Any]
    settingAab: Dict[Any, Any]


class Configuration(BaseModel):
    specification: testSpecification
    settings: testSettings

class TestDocument(BaseModel):
    kind: constr(max_length=32) = Field(default="test", const=True)
    name: constr(max_length=128)
    version: constr(regex=r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
    description: constr(max_length=4096)
    configuration: Configuration