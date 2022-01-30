from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Server(SQLModel, table = True):
    id: int = Field(primary_key=True)
    domain_name: str
    domain_type: Optional[str]
    agency: Optional[int]
    organization: Optional[str]
    catagory: Optional[List[str]] = Field(sa_column=Column(JSON))
    status: str = "LOADING"
    server_log: List["ServerLog"] = Relationship(back_populates="server")
    clicks: int = 0
    ipaddress: Optional[str]
    response_time: Optional[int] = None
    last_checked: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

class ServerLog(SQLModel, table = True):
    id: int = Field(primary_key=True)
    datetime: datetime
    server_id: Optional[int] = Field(default = None, foreign_key="server.id")
    server: Optional[Server] = Relationship(back_populates="server_log")
    response_code: Optional[int]
    response_time: Optional[int]
    ipaddress: Optional[str]
    url: str

    error: Optional[str]