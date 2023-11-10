from typing import Optional

from fastapi.security import OAuth2PasswordBearer

access_token: Optional[str] = None
refresh_token: Optional[str] = None

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
