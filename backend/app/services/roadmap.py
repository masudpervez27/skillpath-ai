import logging

from ..models.schemas import RoadmapMilestone, RoadmapRequest, RoadmapResponse

logger = logging.getLogger(__name__)

ROLE_SKILL_MATRIX = {
    "ai engineer": [
        "python",
        "sql",
        "fastapi",
        "docker",
        "llm",
        "rag",
        "vector database",
        "prompt engineering",
        "evaluation",
        "cloud",
    ],
    "machine learning engineer": [
        "python",
        "sql",
        "feature engineering",
        "model training",
        "mlops",
        "docker",
        "cloud",
        "deployment",
    ],
    "data engineer": [
        "python",
        "sql",
        "etl",
        "airflow",
        "spark",
        "data modeling",
        "cloud",
        "orchestration",
    ],
}

RESOURCE_MAP = {
    "python": ["Python Official Docs", "Real Python"],
    "sql": ["SQLBolt", "Mode SQL Tutorial"],
    "fastapi": ["FastAPI Tutorial", "FastAPI Docs"],
    "docker": ["Docker Getting Started", "Play with Docker"],
    "llm": ["OpenAI API Docs", "LangChain Concepts"],
    "rag": ["LangChain RAG Tutorial", "LlamaIndex RAG Basics"],
    "vector database": ["Qdrant Docs", "Pinecone Learn"],
    "prompt engineering": ["Prompt Engineering Guide", "OpenAI Prompting"],
    "evaluation": ["Ragas Docs", "Promptfoo Docs"],
    "cloud": ["AWS Skill Builder", "Google Cloud Skills Boost"],
    "feature engineering": ["Feature Engineering for ML", "Kaggle Learn"],
    "model training": ["scikit-learn User Guide", "Hands-On ML"],
    "mlops": ["Made with ML", "MLOps Zoomcamp"],
    "deployment": ["BentoML Docs", "Seldon Core Intro"],
    "etl": ["DataTalks ETL Concepts", "Airbyte Docs"],
    "airflow": ["Airflow Docs", "Astronomer Learn"],
    "spark": ["Spark Docs", "Databricks Academy"],
    "data modeling": ["Kimball Dimensional Modeling", "dbt Learn"],
    "orchestration": ["Dagster Docs", "Airflow Concepts"],
}


def _normalize_skills(skills: list[str]) -> list[str]:
    normalized = [s.strip().lower() for s in skills if s and s.strip()]
    unique = sorted(set(normalized))
    return unique


def _target_skills(target_role: str) -> list[str]:
    role_key = target_role.strip().lower()
    if role_key in ROLE_SKILL_MATRIX:
        return ROLE_SKILL_MATRIX[role_key]
    if "ai" in role_key:
        return ROLE_SKILL_MATRIX["ai engineer"]
    if "ml" in role_key:
        return ROLE_SKILL_MATRIX["machine learning engineer"]
    if "data" in role_key:
        return ROLE_SKILL_MATRIX["data engineer"]
    return ROLE_SKILL_MATRIX["ai engineer"]


def _build_milestones(gap_skills: list[str], weeks: int) -> list[RoadmapMilestone]:
    if not gap_skills:
        return [
            RoadmapMilestone(
                week=1,
                focus="Portfolio hardening",
                outcomes=[
                    "Polish two flagship projects",
                    "Document architecture and trade-offs",
                    "Prepare interview narratives",
                ],
                resources=["System Design Primer", "STAR interview prep templates"],
            )
        ]

    chunks: list[list[str]] = []
    chunk_size = max(1, len(gap_skills) // max(1, weeks // 2))
    for idx in range(0, len(gap_skills), chunk_size):
        chunks.append(gap_skills[idx : idx + chunk_size])

    milestones: list[RoadmapMilestone] = []
    current_week = 1
    for group in chunks:
        focus = ", ".join(group)
        outcomes = [f"Build one mini-project using {skill}" for skill in group]
        outcomes.append("Write a short reflection on trade-offs and production concerns")

        resources: list[str] = []
        for skill in group:
            resources.extend(RESOURCE_MAP.get(skill, ["Official documentation", "Community tutorial"]))

        milestones.append(
            RoadmapMilestone(
                week=current_week,
                focus=focus,
                outcomes=outcomes,
                resources=sorted(set(resources))[:4],
            )
        )
        current_week += max(1, weeks // max(1, len(chunks)))

    return milestones


def build_roadmap(payload: RoadmapRequest) -> RoadmapResponse:
    current = _normalize_skills(payload.current_skills)
    target = _target_skills(payload.target_role)

    gap = [skill for skill in target if skill not in current]
    readiness = int(round((1 - (len(gap) / max(1, len(target)))) * 100))
    readiness = max(0, min(100, readiness))

    milestones = _build_milestones(gap, payload.weeks)

    logger.info(
        "Built roadmap for role '%s' with readiness_score=%d and %d milestones",
        payload.target_role,
        readiness,
        len(milestones),
    )

    return RoadmapResponse(
        target_role=payload.target_role,
        current_skills=current,
        gap_skills=gap,
        readiness_score=readiness,
        milestones=milestones,
    )
