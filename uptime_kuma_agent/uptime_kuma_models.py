from pydantic import BaseModel, Field


class UptimeKumaMonitor(BaseModel):
    id: int | None = None
    name: str
    type: str
    url: str | None = None
    interval: int | None = 60
    active: bool | None = True
    accepted_statuscodes: list[str] | None = Field(default_factory=lambda: ["200-299"])


class UptimeKumaMonitorStatus(BaseModel):
    id: int
    name: str
    type: str
    url: str
    status: str
