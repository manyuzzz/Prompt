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
    return {"success": True, "company": company.model_dump()}
