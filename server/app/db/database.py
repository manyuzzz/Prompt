from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from loguru import logger
from app.config.settings import settings


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    from app.models.user import User
    from app.models.resume import Resume, ResumeAnalysis
    from app.models.company import Company
    from app.models.roadmap import Roadmap
    from app.models.conversation import Conversation
    from app.models.interview import Interview
    from app.models.coding import CodingProblem, Submission
    from app.models.aptitude import AptitudeQuestion, AptitudeAttempt
    from app.models.progress import Progress

    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User, Resume, ResumeAnalysis, Company, Roadmap,
            Conversation, Interview, CodingProblem, Submission,
            AptitudeQuestion, AptitudeAttempt, Progress,
        ],
    )
    logger.info(f"MongoDB connected: {settings.MONGODB_URI}")
