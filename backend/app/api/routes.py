import logging

from fastapi import APIRouter

from ..models.schemas import RoadmapRequest, RoadmapResponse
from ..services.roadmap import build_roadmap

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}


@router.post("/roadmap")
async def roadmap_route(payload: RoadmapRequest) -> RoadmapResponse:
    logger.info("Roadmap endpoint called (current_skills=%d, target_role=%s)", len(payload.current_skills), payload.target_role)
    result = build_roadmap(payload)
    logger.info("Roadmap generated with %d gap skills", len(result.gap_skills))
    return result
