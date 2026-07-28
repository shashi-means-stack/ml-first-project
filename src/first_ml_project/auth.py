from __future__ import annotations

import os
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

API_TOKEN = os.getenv("API_TOKEN", "demo-token")
security = HTTPBearer(auto_error=False)


def require_api_token(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    token: str | None = Query(default=None),
) -> None:
    configured_token = (API_TOKEN or "demo-token").strip()
    provided = None
    if credentials is not None:
        provided = credentials.credentials
    elif token is not None:
        provided = token
    elif request.headers.get("x-api-token"):
        provided = request.headers.get("x-api-token")

    if provided is None:
        if configured_token == "demo-token":
            return
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if provided.strip() != configured_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
            headers={"WWW-Authenticate": "Bearer"},
        )
