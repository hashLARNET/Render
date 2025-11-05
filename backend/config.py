from pydantic_settings import BaseSettings
from typing import List
from urllib.parse import quote_plus
import os

def encode_database_url(url: str) -> str:
    """Encode special characters in database URL"""
    if '#' in url:
        parts = url.split('@')
        if len(parts) == 2:
            creds_part = parts[0]
            host_part = parts[1]
            if ':' in creds_part:
                protocol_user, password = creds_part.rsplit(':', 1)
                encoded_password = quote_plus(password)
                return f"{protocol_user}:{encoded_password}@{host_part}"
    return url

class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    
    # Database
    database_url: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.database_url:
            self.database_url = encode_database_url(self.database_url)
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS - SIMPLIFICADO TEMPORALMENTE
    netlify_url: str = ""
    render_external_url: str = ""
    
    @property
    def allowed_origins(self) -> List[str]:
        # ✅ VERSIÓN SIMPLIFICADA - PERMITIR TODO TEMPORALMENTE
        return ["*"]

settings = Settings()
