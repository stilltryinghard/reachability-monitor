from enum import Enum

from pydantic import BaseModel, Field


class VantageMode(str, Enum):
    pull = "pull"
    push = "push"
    
    
class Country(str, Enum):
    ru = "RU"
    pl = "PL"
    
    
class VantagePointCreate(BaseModel):
    slug: str = Field(min_length=2, max_length=40, pattern=r"^[a-z0-9-]+$")
    name: str
    country: Country
    operator: str
    network_type: str
    mode: VantageMode
    
    
class VantagePointOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    country: Country
    operator: str
    network_type: str
    mode: VantageMode
    
    model_config = {"populate_by_name": True}
    