from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MeasurementResult(str, Enum):
    ok = "ok"
    timeout = "timeout"
    connection_error = "connection_error"
    request_error = "request_error"

class MeasurementCreate(BaseModel):
    measurement_id: str
    resource_id: str
    vantage_id: str
    measured_at: datetime
    result: MeasurementResult
    details: dict
