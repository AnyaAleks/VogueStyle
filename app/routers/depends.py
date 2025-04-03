from fastapi import Depends
from db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]