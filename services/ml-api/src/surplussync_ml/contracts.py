from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ForecastFeatures(BaseModel):
    school_id: str = "lhphs"
    date: date
    enrolled: int = Field(default=820, ge=1)
    eligible: int = Field(default=760, ge=1)
    normal_prep: int = Field(default=730, ge=0)
    expected_attendance: int | None = Field(default=None, ge=0)
    is_exam: bool = False
    trip_students: int = Field(default=0, ge=0)
    early_dismissal: bool = False
    assembly_students: int = Field(default=0, ge=0)
    sports_students: int = Field(default=0, ge=0)
    rain_probability: float = Field(default=0.0, ge=0, le=1)
    rain_inches: float = Field(default=0.0, ge=0)
    temperature_f: float = 55.0
    menu_name: str = "Chicken & rice"
    menu_popularity: float = Field(default=1.0, ge=0.5, le=1.5)
    recent_attendance_7d: float = Field(default=705.0, ge=0)
    recent_attendance_14d: float = Field(default=702.0, ge=0)

    @model_validator(mode="after")
    def validate_school_bounds(self) -> ForecastFeatures:
        if self.eligible > self.enrolled:
            raise ValueError("eligible cannot exceed enrolled")
        return self


class MenuPrediction(BaseModel):
    item: str
    recommended: int


class Influence(BaseModel):
    factor: str
    direction: Literal["up", "down"]
    magnitude: int
    note: str


class SimilarDay(BaseModel):
    date: date
    attendance: int
    note: str


class ForecastResponse(BaseModel):
    date: date
    expectedAttendance: int
    intervalLow: int
    intervalHigh: int
    recommendedPrep: int
    shortageProb: float
    largeSurplusProb: float
    preventableSurplus: int
    risk: Literal["low", "moderate", "high", "critical"]
    dataQuality: Literal["low", "medium", "high"]
    modelVersion: str
    menu: list[MenuPrediction]
    influences: list[Influence]
    similarDays: list[SimilarDay]
    approvalRequired: bool = True
    decisionStatus: Literal["PROPOSED"] = "PROPOSED"
    safetyFloorApplied: bool
    generatedAt: datetime


class WhatIfRequest(BaseModel):
    base: ForecastFeatures
    changes: dict[str, int | float | bool | str]


class ModelMetadata(BaseModel):
    modelVersion: str
    trained: bool
    metrics: dict[str, float]
    featureNames: list[str]
    categoricalFeatures: list[str]
    trainingRows: int
    dataWindow: dict[str, str]
