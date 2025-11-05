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
    # Supabase - se cargan de las variables de Render
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "") 
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # Database - Render provee DATABASE_URL automáticamente si usas su DB
    # Pero tú usas Supabase, así que no necesitas esta línea:
    # database_url: str = os.getenv("DATABASE_URL", "")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    @property
    def allowed_origins(self) -> List[str]:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "http://localhost:8080", 
            "http://127.0.0.1:8080"
        ]
        
        # Agregar dominio de Netlify desde variables de Render
        netlify_url = os.getenv("NETLIFY_URL", "")
        if netlify_url:
            origins.extend([
                f"https://{netlify_url}",
                f"http://{netlify_url}"
            ])
        
        # Agregar dominio de Render
        render_url = os.getenv("RENDER_EXTERNAL_URL", "")
        if render_url:
            origins.append(render_url)
            
        return origins

# No necesita Config con env_file porque usa variables de entorno del sistema
settings = Settings()
