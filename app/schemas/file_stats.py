from datetime import datetime

from pydantic import BaseModel


class FileStatsResponse(BaseModel):
    name: str
    format: str
    size: int
    ctime: datetime
