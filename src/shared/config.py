"""
Configuration Management Module

Use Pydantic to safely load and validate data from .env for application use
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application setting schema

    Attributes:
        openai_api_key(str)
        openai_model_name(str)
        firecrawl_api_key
        langchain_api_key
        langchain_tracing_v2
    """
    openai_api_key: str = Field(..., description="OpenAI API Key")
    openai_model_name: str = Field(
        "gpt-4.1-mini", description="Default OpenAI model")
    firecrawl_api_key: str = Field(...,
                                   description="Firecrawl API for web scraping service")
    langchain_tracing_v2: bool = Field(
        False, description="Enable Langsmith tracing")
    langchain_api_key: Optional[str] = Field(
        None, description="Langsmith API Key")

    azure_postgres_connection_string: Optional[str] = Field(
        None, description="Connection string for Azure Postgres Database")

    azure_blob_storage_connection_string: Optional[str] = Field(
        None, description="Connection string for Azure Blob Storage Container")

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """
    Creates and caches the settings object.

    Using lru_cache ensures that we only read the .env once on startup
    """
    return Settings()


# Instantiate settings object
settings = get_settings()
