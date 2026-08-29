"""Configuration management for flight pipeline."""

import os
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class AWSConfig:
    """AWS configuration."""
    
    ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "")
    S3_RAW_PATH: str = os.getenv("AWS_S3_RAW_PATH", "s3://bucket/raw/")
    S3_PROCESSED_PATH: str = os.getenv("AWS_S3_PROCESSED_PATH", "s3://bucket/processed/")
    
    @classmethod
    def validate(cls) -> None:
        """Validate all required AWS configuration."""
        required = [
            "ACCESS_KEY_ID",
            "SECRET_ACCESS_KEY",
            "S3_BUCKET",
        ]
        missing = [k for k in required if not getattr(cls, k)]
        if missing:
            raise EnvironmentError(
                f"Missing AWS configuration: {', '.join(missing)}. "
                "Please set in .env file"
            )


class DatabricksConfig:
    """Databricks configuration."""
    
    HOST: str = os.getenv("DATABRICKS_HOST", "")
    TOKEN: str = os.getenv("DATABRICKS_TOKEN", "")
    CLUSTER_ID: str = os.getenv("DATABRICKS_CLUSTER_ID", "")
    
    @classmethod
    def validate(cls) -> None:
        """Validate all required Databricks configuration."""
        required = ["HOST", "TOKEN"]
        missing = [k for k in required if not getattr(cls, k)]
        if missing:
            raise EnvironmentError(
                f"Missing Databricks configuration: {', '.join(missing)}. "
                "Please set in .env file"
            )


class SnowflakeConfig:
    """Snowflake configuration."""
    
    ACCOUNT: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    USER: str = os.getenv("SNOWFLAKE_USER", "")
    PASSWORD: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    WAREHOUSE: str = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "")
    SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "")
    ROLE: str = os.getenv("SNOWFLAKE_ROLE", "")
    
    @classmethod
    def validate(cls) -> None:
        """Validate all required Snowflake configuration."""
        required = [
            "ACCOUNT",
            "USER",
            "PASSWORD",
            "DATABASE",
            "SCHEMA",
        ]
        missing = [k for k in required if not getattr(cls, k)]
        if missing:
            raise EnvironmentError(
                f"Missing Snowflake configuration: {', '.join(missing)}. "
                "Please set in .env file"
            )


class AppConfig:
    """Application configuration."""
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_RETRY_ATTEMPTS: int = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
    API_TIMEOUT_SECONDS: int = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
    
    # API endpoints
    OPENSKY_API_URL: str = "https://opensky-network.org/api/states/all"
    
    # Data configuration
    BATCH_SIZE: int = 1000
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == "development"


def validate_all_config() -> None:
    """Validate all configuration before running application."""
    try:
        AWSConfig.validate()
        logger.info("✓ AWS configuration validated")
    except EnvironmentError as e:
        logger.error(f"✗ AWS configuration error: {e}")
        raise
    
    try:
        DatabricksConfig.validate()
        logger.info("✓ Databricks configuration validated")
    except EnvironmentError as e:
        logger.warning(f"⚠ Databricks configuration error: {e}")
        # Databricks is optional for some workflows
    
    try:
        SnowflakeConfig.validate()
        logger.info("✓ Snowflake configuration validated")
    except EnvironmentError as e:
        logger.warning(f"⚠ Snowflake configuration error: {e}")
        # Snowflake is optional for some workflows
    
    logger.info(f"✓ Application configured for {AppConfig.ENVIRONMENT} environment")
