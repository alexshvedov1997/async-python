from fastapi.security import OAuth2PasswordBearer


access_token = None
refresh_token = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
