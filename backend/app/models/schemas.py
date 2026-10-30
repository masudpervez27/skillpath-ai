from pydantic import BaseModel, Field


class RoadmapRequest(BaseModel):
    current_skills: list[str] = Field(default_factory=list)
    target_role: str = Field(min_length=2, max_length=120)
    weeks: int = Field(default=8, ge=4, le=24)


class RoadmapMilestone(BaseModel):
    week: int
    focus: str
    outcomes: list[str]
    resources: list[str]


class RoadmapResponse(BaseModel):
    target_role: str
    current_skills: list[str]
    gap_skills: list[str]
    readiness_score: int
    milestones: list[RoadmapMilestone]
