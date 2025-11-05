from pydantic_settings import BaseSettings
from typing import List
from urllib.parse import quote_plus

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
    # Supabase - Para API y autenticación
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    
    # Database URL - Para SQLAlchemy (conexión directa a PostgreSQL de Supabase)
    database_url: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Codificar database_url si existe (para caracteres especiales como #)
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
    
    # CORS - Placeholder para Netlify
    netlify_url: str = "mi-app-inventario.netlify.app"
    
 @property
def allowed_origins(self) -> List[str]:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://690ba088ef32910008f4b042--scintillating-bubblegum-5a4b8b.netlify.app"
    ]
    
    # Agregar dominio de Netlify desde variables
    if self.netlify_url:
        origins.extend([
            f"https://{self.netlify_url}",
            f"http://{self.netlify_url}"
        ])
    
    # Agregar dominio de Render
    if self.render_external_url:
        origins.append(self.render_external_url)
        
    return origins
    
    # Campo opcional para Render URL
    render_external_url: str = ""

settings = Settings()
