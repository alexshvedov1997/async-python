from pydantic import BaseModel, Field

password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class User(BaseModel):
    username: str
    password: str = Field(regex=password_regex)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class File(BaseModel):
    created_at: str
    name: str
    size: int


class ServiceAvailabiltySchema(BaseModel):
    psql: bool = False
    redis: bool = False
    s3: bool = False
