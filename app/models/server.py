from sqlmodel import SQLModel, Field, JSON, Relationship, VARCHAR
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Column


class ServerCatagoryLink(SQLModel, table=True):
    server_id: Optional[int] = Field(
        default=None, foreign_key="server.id", primary_key=True
    )
    catagory_id: Optional[int] = Field(
        default=None, foreign_key="catagory.id", primary_key=True
    )

class ServerOrganizationLink(SQLModel, table=True):
    server_id: Optional[int] = Field(
        default=None, foreign_key="server.id", primary_key=True
    )
    organization_id: Optional[int] = Field(
        default=None, foreign_key="organization.id", primary_key=True
    )

class Catagory(SQLModel, table = True):
    id: int = Field(primary_key = True)
    title: str = Field(sa_column=Column("title", String(255), unique=True))
    meta_ref: str = Field(sa_column=Column("meta_ref", String(255), unique=True))
    color: str
    servers: List["Server"] = Relationship(back_populates="catagories", link_model=ServerCatagoryLink)

class SaveCatagory(SQLModel):
    title: str
    color: str

class Organization(SQLModel, table = True):
    id: int = Field(primary_key = True)
    title: str
    agency: str
    description: str
    servers: List["Server"] = Relationship(back_populates="organizations", link_model=ServerOrganizationLink)

class Server(SQLModel, table = True):
    id: int = Field(primary_key=True)
    domain_name: str
    domain_type: Optional[str]
    agency: Optional[int]
    organization: Optional[str]
    status: str = "LOADING"
    server_log: List["ServerLog"] = Relationship(back_populates="server")
    clicks: int = 0
    ipaddress: Optional[str]
    response_time: Optional[int] = None
    last_checked: Optional[datetime]
    catagories: List["Catagory"] = Relationship(back_populates="servers", link_model=ServerCatagoryLink)
    organizations: List["Organization"] = Relationship(back_populates="servers", link_model=ServerOrganizationLink)

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