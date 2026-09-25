"""
PAIMANA AI - JWT Authentication & RBAC helpers
Uses PyJWT (already in dependencies via jwt) + stdlib pbkdf2 for password hashing.
"""
import os
import re
import time
import hmac
import hashlib
import base64
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

try:
    import jwt  # PyJWT 2.x
    _HAS_JWT = True
except ImportError:
    jwt = None  # type: ignore
    _HAS_JWT = False

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-generate-with-openssl-rand-hex-32")
JWT_ALGO = "HS256"
JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES", "120"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

security = HTTPBearer(auto_error=False)

try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    bcrypt = None  # type: ignore
    _HAS_BCRYPT = False

def _hash_pwd(pwd: str, salt: str = "paimana-salt-v1") -> str:
    dk = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt.encode(), 100000)
    return base64.b64encode(dk).decode()

DEMO_PASSWORD_HASH = _hash_pwd("Paimana@123")
DEMO_PWD_SALT = "paimana-salt-v1"

def hash_password(plain: str) -> str:
    # Use deterministic PBKDF2 to ensure universal compatibility across all Python environments
    return _hash_pwd(plain, DEMO_PWD_SALT)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        if _HAS_BCRYPT and bcrypt is not None and (
            hashed.startswith("$2a$") or hashed.startswith("$2b$") or hashed.startswith("$2y$")
        ):
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
        return hmac.compare_digest(_hash_pwd(plain, DEMO_PWD_SALT), hashed)
    except Exception:
        return False

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)

def create_access_token(payload: Dict[str, Any], expires_minutes: int = JWT_EXPIRY_MINUTES) -> str:
    now = int(time.time())
    to_encode = {**payload, "iat": now, "exp": now + expires_minutes * 60, "iss": "paimana-ai"}
    if _HAS_JWT:
        return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)
    # Fallback pure-python HS256
    import json
    header = _b64url_encode(json.dumps({"alg": JWT_ALGO, "typ": "JWT"}).encode())
    body = _b64url_encode(json.dumps(to_encode).encode())
    sig = _b64url_encode(hmac.new(JWT_SECRET.encode(), f"{header}.{body}".encode(), hashlib.sha256).digest())
    return f"{header}.{body}.{sig}"

def decode_token(token: str) -> Dict[str, Any]:
    if _HAS_JWT:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO], options={"require": ["exp", "iat"]})
    import json
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid token format")
    header_b, body_b, sig_b = parts
    expected_sig = _b64url_encode(hmac.new(JWT_SECRET.encode(), f"{header_b}.{body_b}".encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(expected_sig, sig_b):
        raise ValueError("Invalid signature")
    payload = json.loads(_b64url_decode(body_b).decode())
    if payload.get("exp", 0) < int(time.time()):
        raise ValueError("Token expired")
    return payload

def parse_clearance_level(level_str: str) -> int:
    m = re.search(r"Level-(\d+)", level_str or "")
    return int(m.group(1)) if m else 0

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Dict[str, Any]:
    # Allow unauthenticated in development for GET read-only endpoints; mutating endpoints must require auth explicitly
    # This dependency when used will enforce auth.
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing authentication token. Please login at /api/auth/login.")
    token = credentials.credentials
    # Legacy demo tokens (jwt-*) without signature - reject
    if token.startswith("jwt-") and token.count(".") != 2:
        raise HTTPException(status_code=401, detail="Legacy demo token rejected. Please login again to get a signed JWT.")
    try:
        data = decode_token(token)
        return data
    except Exception as e:
        # Handle both PyJWT and fallback errors uniformly
        msg = str(e).lower()
        if "expired" in msg:
            raise HTTPException(status_code=401, detail="Token expired. Please login again.")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def require_min_clearance(min_level: int):
    async def _checker(user: Dict[str, Any] = Depends(get_current_user)):
        lvl = parse_clearance_level(user.get("clearance_level", ""))
        if lvl < min_level:
            raise HTTPException(status_code=403, detail=f"Insufficient clearance. Requires Level-{min_level}+, your level is Level-{lvl}.")
        return user
    return _checker

def require_role(allowed_roles: list[str]):
    """
    Validates JWT role claims.
    Returns a 403 Forbidden statutory clearance error if unauthorized.
    """
    normalized_allowed = set(allowed_roles)
    for r in allowed_roles:
        if r in ("admin", "MoSPI Registry Official", "Cabinet Review Authority"):
            normalized_allowed.add("admin")
        else:
            normalized_allowed.add("employee")

    async def _role_checker(user: Dict[str, Any] = Depends(get_current_user)):
        user_role = user.get("role", "")
        mapped_role = "admin" if user_role in ("admin", "Cabinet Review Authority", "MoSPI Registry Official") else "employee"

        if mapped_role not in normalized_allowed and user_role not in normalized_allowed:
            raise HTTPException(
                status_code=403,
                detail=f"Statutory clearance error: Insufficient administrative privileges. Required statutory role in {allowed_roles}, but current officer role is '{user_role}'."
            )
        return user
    return _role_checker

# Singleton for optional auth (read endpoints that allow anonymous)
async def get_optional_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[Dict[str, Any]]:
    if not credentials or not credentials.credentials:
        return None
    try:
        return decode_token(credentials.credentials)
    except Exception:
        return None
