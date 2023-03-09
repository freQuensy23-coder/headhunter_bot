from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from HHApi.Models.Logos import LogoUrls


class Salary(BaseModel):
    to: Optional[Any] | None
    from_: Optional[int] | None = Field(..., alias='from')
    currency: Optional[str] | None
    gross: Optional[bool] | None


class InsiderInterview(BaseModel):
    id: Optional[str] | None
    url: Optional[str] | None


class Area(BaseModel):
    url: Optional[str] | None
    id: Optional[str] | None
    name: Optional[str] | None


class Employer(BaseModel):
    logo_urls: Optional[LogoUrls] | None
    name: Optional[str] | None
    url: Optional[str] | None
    alternate_url: Optional[str] | None
    id: Optional[str] | None
    trusted: Optional[bool] | None


class Phone(BaseModel):
    country: Optional[str] | None
    city: Optional[str] | None
    number: Optional[str] | None
    comment: Optional[Any] | None


class Contacts(BaseModel):
    name: Optional[str] | None
    email: Optional[str] | None
    phones: Optional[List[Phone]] | None


class MetroStation(BaseModel):
    station_id: Optional[str] | None
    station_name: Optional[str] | None
    line_id: Optional[str] | None
    line_name: Optional[str] | None
    lat: Optional[float] | None
    lng: Optional[float] | None


class Address(BaseModel):
    city: Optional[str] | None
    street: Optional[str] | None
    building: Optional[str] | None
    description: Optional[str] | None
    lat: Optional[float] | None
    lng: Optional[float] | None
    metro_stations: Optional[List[MetroStation]] | None


class Department(BaseModel):
    id: Optional[str] | None
    name: Optional[str] | None


class Type(BaseModel):
    id: Optional[str] | None
    name: Optional[str] | None


class Snippet(BaseModel):
    requirement: Optional[str] | None
    responsibility: Optional[str] | None | None


class Schedule(BaseModel):
    id: Optional[str] | None
    name: Optional[str] | None


class Counters(BaseModel):
    responses: Optional[int] | None


class ShortVacancy(BaseModel):
    salary: Optional[Salary] | None
    name: Optional[str] | None
    insider_interview: Optional[InsiderInterview] | None
    area: Optional[Area] | None
    url: Optional[str] | None
    published_at: Optional[str] | None
    relations: Optional[List] | None
    employer: Optional[Employer] | None
    contacts: Optional[Contacts] | None
    response_letter_required: Optional[bool] | None
    address: Optional[Address] | None
    sort_point_distance: Optional[float] | None
    alternate_url: Optional[str] | None
    apply_alternate_url: Optional[str] | None
    department: Optional[Department] | None
    type: Optional[Type] | None
    id: Optional[str] | None
    has_test: Optional[bool] | None
    response_url: Optional[Any] | None
    snippet: Optional[Snippet] | None
    schedule: Optional[Schedule] | None
    counters: Optional[Counters] | None


class SearchResponse(BaseModel):
    per_page: Optional[int] | None
    items: Optional[List[ShortVacancy]] | None
    page: Optional[int] | None
    pages: Optional[int] | None
    found: Optional[int] | None
    clusters: Optional[Any] | None
    arguments: Optional[Any] | None
