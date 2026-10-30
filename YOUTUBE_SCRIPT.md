# SkillPath AI - YouTube Transcript Script

## Title
Build an AI Learning Roadmap Generator with Skills-Gap Analysis (Project 08)

## Intro
In this project we implement SkillPath AI from the portfolio plan.

Input:
- current skills,
- target role,
- timeline in weeks.

Output:
- gap skills,
- readiness score,
- weekly roadmap milestones,
- targeted learning resources.

## Why this matters
Generic roadmaps are not useful. We need role-targeted and skill-aware sequencing.

## Backend flow
1. Normalize current skills.
2. Map target role to required skills.
3. Compute skill gaps.
4. Calculate readiness score.
5. Generate milestones and resources.

This returns a structured response that is easy to render in frontend.

## Frontend flow
The UI captures role, skills, and weeks, then calls POST /api/roadmap.

It renders:
- readiness score,
- gap skills,
- milestone cards with outcomes and resources.

## Logging
Backend logs request context and roadmap completion.
Frontend logs request lifecycle and API errors using VITE_LOG_LEVEL.

## Outro
This feature slice gives you a portfolio-ready recommendation workflow and a clean foundation for graph-based skill visualization next.
