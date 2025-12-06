from pydantic import BaseModel
from typing import Dict, Any


class RenderRequest(BaseModel):
    data: Dict[str, Any]
