from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth_service import (
    register_user, verify_email_token, login_user
)
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    VerifyEmailRequest, ForgotPasswordRequest, ResetPasswordRequest,
    RefreshRequest, MessageResponse
)
from app.utils.security import create_access_token, decode_token

router = APIRouter()

@router.post("/register", response_model=MessageResponse)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await register_user(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        db=db,
    )
    # In dev mode: auto-verify token
    from app.utils.security import create_access_token
    verify_token = create_access_token({"sub": str(user.id), "purpose": "email_verify"})
    return {"message": f"Registration successful. Dev verify token: {verify_token}"}

@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(
    request: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    await verify_email_token(request.token, db)
    return {"message": "Email verified successfully. You can now log in."}

@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await login_user(request.email, request.password, db)

@router.post("/refresh", response_model=dict)
async def refresh_token(request: RefreshRequest):
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_access = create_access_token({"sub": payload["sub"], "role": payload.get("role")})
        return {"access_token": new_access, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout", response_model=MessageResponse)
async def logout():
    # Stateless JWT — client deletes token
    return {"message": "Logged out successfully"}

@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(request: ForgotPasswordRequest):
    # In dev: just return success (email sending added later)
    return {"message": "If this email exists, a reset link has been sent."}

@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest):
    # In dev: placeholder
    return {"message": "Password reset functionality will be implemented with email service."}
