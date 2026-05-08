import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserProfile, Consent
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.config import settings

async def register_user(
    email: str,
    password: str,
    full_name: str,
    db: AsyncSession
) -> User:
    # Check duplicate
    result = await db.execute(select(User).where(User.email == email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate password
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Create user
    user = User(
        email=email.lower().strip(),
        password_hash=hash_password(password),
        role="student",
        is_active=False,
        is_verified=False,
    )
    db.add(user)
    await db.flush()
    
    # Create profile
    profile = UserProfile(
        user_id=user.id,
        full_name=full_name,
    )
    db.add(profile)
    
    # Record DPDP consent
    consent = Consent(
        user_id=user.id,
        consent_type="dpdp_terms",
        version="1.0",
        consented=True,
    )
    db.add(consent)
    
    await db.commit()
    await db.refresh(user)
    return user

async def verify_email_token(token: str, db: AsyncSession) -> User:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        token_type = payload.get("purpose")
        if token_type != "email_verify":
            raise HTTPException(status_code=400, detail="Invalid token type")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_verified = True
    user.is_active = True
    user.email_verified_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return user

async def login_user(email: str, password: str, db: AsyncSession) -> dict:
    result = await db.execute(select(User).where(User.email == email.lower().strip()))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # For development: auto-activate if not verified
    if not user.is_active:
        if settings.APP_ENV == "development":
            user.is_active = True
            user.is_verified = True
            await db.commit()
        else:
            raise HTTPException(status_code=401, detail="Please verify your email first")
    
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    token_data = {"sub": str(user.id), "role": user.role.value}
    
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value,
        }
    }

async def get_current_user(token: str, db: AsyncSession) -> User:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user
