from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from .Logos import LogoUrls


class BillingType(BaseModel):
    id: str
    name: str


class Area(BaseModel):
    id: str
    name: str
    url: str


class Type(BaseModel):
    id: str
    name: str


class Experience(BaseModel):
    id: str
    name: str


class Schedule(BaseModel):
    id: str
    name: str


class Employment(BaseModel):
    id: str
    name: str


class ProfessionalRole(BaseModel):
    id: str
    name: str


class Employer(BaseModel):
    id: str
    name: str
    url: str
    alternate_url: str
    logo_urls: LogoUrls
    vacancies_url: str
    trusted: bool


class Vacancy(BaseModel):
    id: Optional[str] = None
    premium: Optional[bool] = None
    billing_type: Optional[BillingType] = None
    relations: Optional[List] = None
    name: Optional[str] = None
    insider_interview: Optional[Any] = None
    response_letter_required: Optional[bool] = None
    area: Optional[Area] = None
    salary: Optional[Any] = None
    type: Optional[Type] = None
    address: Optional[Any] = None
    allow_messages: Optional[bool] = None
    experience: Optional[Experience] = None
    schedule: Optional[Schedule] = None
    employment: Optional[Employment] = None
    department: Optional[Any] = None
    contacts: Optional[Any] = None
    description: Optional[str] = None
    branded_description: Optional[Any] = None
    vacancy_constructor_template: Optional[Any] = None
    key_skills: Optional[List] = None
    accept_handicapped: Optional[bool] = None
    accept_kids: Optional[bool] = None
    archived: Optional[bool] = None
    response_url: Optional[Any] = None
    specializations: Optional[List] = None
    professional_roles: Optional[List[ProfessionalRole]] = None
    code: Optional[Any] = None
    hidden: Optional[bool] = None
    quick_responses_allowed: Optional[bool] = None
    driver_license_types: Optional[List] = None
    accept_incomplete_resumes: Optional[bool] = None
    employer: Optional[Employer] = None
    published_at: Optional[str] = None
    created_at: Optional[str] = None
    initial_created_at: Optional[str] = None
    negotiations_url: Optional[Any] = None
    suitable_resumes_url: Optional[Any] = None
    apply_alternate_url: Optional[str] = None
    has_test: Optional[bool] = None
    test: Optional[Any] = None
    alternate_url: Optional[str] = None
    working_days: Optional[List] = None
    working_time_intervals: Optional[List] = None
    working_time_modes: Optional[List] = None
    accept_temporary: Optional[bool] = None
    languages: Optional[List] = None
