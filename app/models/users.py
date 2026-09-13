from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str | None=None
    password_hash: str
    full_name: str | None=None
    bio: str
    is_active: bool
    is_superuser: bool = False

class Post(BaseModel):
    id: int
    user_id: int
    title: str
    slug: str
    content: str
    excerpt: str | None=None
    status: str = "draft"
    image: str
    views: int
    created_at: datetime
    updated_at: datetime
    published_at: datetime
    

