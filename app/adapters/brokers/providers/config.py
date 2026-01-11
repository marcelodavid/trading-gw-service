from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FXCM_USER_ID: str = "demo"
    FXCM_PASSWORD: str = "demo"
    FXCM_URL: str = "http://www.fxcorporate.com/Hosts.jsp"
    FXCM_CONNECTION: str = "Demo"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        prefix = "TRADING_GATEWAY_"


settings = Settings()
