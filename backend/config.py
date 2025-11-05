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
    
    # Database - Render automáticamente provee DATABASE_URL
    database_url: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Usar DATABASE_URL de Render si está disponible
        render_db_url = os.getenv('DATABASE_URL')
        if render_db_url:
            self.database_url = encode_database_url(render_db_url)
        elif self.database_url:
            self.database_url = encode_database_url(self.database_url)
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS - Configuración para Render + Netlify
    @property
    def allowed_origins(self) -> List[str]:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "http://localhost:8080",
            "http://127.0.0.1:8080"
        ]
        
        # Agregar dominio de Netlify desde variables de entorno
        netlify_url = os.getenv("NETLIFY_URL", "")
        if netlify_url:
            origins.extend([
                f"https://{netlify_url}",
                f"http://{netlify_url}"
            ])
        
        # Agregar dominio de Render si existe
        render_url = os.getenv("RENDER_EXTERNAL_URL", "")
        if render_url:
            origins.append(render_url)
            
        return origins

    class Config:
        env_file = ".env"

settings = Settings()
