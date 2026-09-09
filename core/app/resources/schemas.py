from pydantic import BaseModel, Field


class ResourceCreate(BaseModel):
    name: str
    url: str
    check_interval_sec: int
    slug: str = Field(
        min_length=2,
        max_length=40,
        pattern=r"^[a-zA-Z0-9_-]+$", #только латиница, цифры, дефис и нижнее подчеркивание.
    )
    
    
class ResourceOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    url: str
    check_interval_sec: int
    enabled: bool
    
    model_config = {"populate_by_name": True} #разрешает заполнять поле и по имени id, и по алиасу _id.
    
    
class ResourceForAgent(BaseModel):
    id: str = Field(alias="_id")
    url: str
    
    model_config = {"populate_by_name": True}