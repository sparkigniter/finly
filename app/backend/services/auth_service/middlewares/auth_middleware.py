from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.backend.services.auth_service.token import Token
from app.backend.services.container import container


# Standard FastAPI helper to handle 'Bearer <token>' headers
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Middleware-style dependency to verify the token.
    """
    token_string = credentials.credentials
    auth_service_provider = container.auth_service_provider

    if not auth_service_provider.verify_token(token_string):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(tokenString=token_string)