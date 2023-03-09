from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class LogoUrls(BaseModel):
    size90: Optional[str] | None = Field(..., alias='90')
    size240: Optional[str] | None = Field(..., alias='240')
    original: Optional[str] | None
