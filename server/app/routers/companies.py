from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.models.company import Company
from app.models.user import User
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/companies", tags=["companies"])


@router.get("/")
async def get_companies(
    search: Optional[str] = None,
    tier: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
):
    filters = []
    if tier:
        filters.append(Company.tier == tier)

    companies = await Company.find(*filters).limit(limit).to_list()
    if search:
        search_lower = search.lower()
        companies = [c for c in companies if search_lower in c.name.lower()]

    return {"success": True, "companies": [
        {
            "id": str(c.id), "name": c.name, "slug": c.slug,
            "description": c.description, "industry": c.industry,
            "tier": c.tier, "size": c.size, "headquarters": c.headquarters,
            "logo": c.logo,
        }
        for c in companies
    ]}


@router.get("/{slug}")
async def get_company(slug: str, current_user: User = Depends(get_current_user)):
    company = await Company.find_one(Company.slug == slug)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    salary = None
    if company.salary_range:
        sr = company.salary_range
        salary = {"min": sr.min, "max": sr.max, "currency": sr.currency} if hasattr(sr, 'min') else str(sr)

    return {"success": True, "company": {
        "id": str(company.id),
        "name": company.name,
        "slug": company.slug,
        "logo": company.logo,
        "description": company.description,
        "website": company.website,
        "industry": company.industry,
        "size": company.size,
        "headquarters": company.headquarters,
        "overview": company.overview,
        "tier": company.tier,
        "is_verified": company.is_verified,
        "roles": [
            {"title": r.title, "type": r.type, "description": r.description}
            if hasattr(r, 'title') else {"title": str(r)}
            for r in (company.roles or [])
        ],
        "eligibility": company.eligibility or {},
        "recruitment_process": [
            {"stage": s.stage, "description": s.description, "duration": s.duration, "tips": s.tips}
            if hasattr(s, 'stage') else {"stage": str(s)}
            for s in (company.recruitment_process or [])
        ],
        "aptitude_pattern": company.aptitude_pattern,
        "coding_pattern": company.coding_pattern,
        "technical_topics": company.technical_topics or [],
        "hr_topics": company.hr_topics or [],
        "frequently_asked_topics": company.frequently_asked_topics or [],
        "preparation_strategy": company.preparation_strategy,
        "salary_range": salary,
    }}
