"""
配置文件
使用环境变量管理敏感信息
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置"""
    # JWT 配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fastadmin_secret_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/fastadmin.db")
    
    # CORS 配置
    CORS_ORIGINS: list = ["*"]  # 生产环境应限制具体域名
    
    class Config:
        case_sensitive = True

settings = Settings()
