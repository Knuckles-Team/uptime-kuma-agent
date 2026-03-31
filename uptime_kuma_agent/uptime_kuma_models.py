from typing import List, Optional
from pydantic import BaseModel, Field


class UptimeKumaMonitor(BaseModel):
    id: Optional[int] = None
    name: str
    type: str
    url: Optional[str] = None
    interval: Optional[int] = 60
    active: Optional[bool] = True
    accepted_statuscodes: Optional[List[str]] = Field(
        default_factory=lambda: ["200-299"]
    )


class UptimeKumaMonitorStatus(BaseModel):
    id: int
    name: str
    type: str
    url: str
    status: str
