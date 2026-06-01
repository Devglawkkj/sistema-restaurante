# Configuracao de aplicacao baseada em variaveis de ambiente.
# Essa configuracao inclui URL do banco, chave secreta e parametros de expiracao de token.
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    class Config:
        env_file = ".env"


settings = Settings()
