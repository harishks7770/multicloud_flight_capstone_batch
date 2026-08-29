"""Secrets management utilities for production deployments."""

import boto3
import json
from typing import Dict, Optional, Any
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SecretsManager:
    """Manage secrets using AWS Secrets Manager."""
    
    def __init__(self, region_name: str = "us-east-1"):
        """Initialize Secrets Manager client.
        
        Args:
            region_name: AWS region name
        """
        self.client = boto3.client("secretsmanager", region_name=region_name)
    
    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve secret from AWS Secrets Manager.
        
        Args:
            secret_name: Name of the secret
            
        Returns:
            Dictionary containing secret key-value pairs
            
        Raises:
            ClientError: If secret cannot be retrieved
        """
        try:
            logger.info(f"Retrieving secret: {secret_name}")
            response = self.client.get_secret_value(SecretId=secret_name)
            
            if "SecretString" in response:
                secret = json.loads(response["SecretString"])
                logger.info(f"✓ Secret retrieved: {secret_name}")
                return secret
            else:
                logger.error(f"✗ Secret {secret_name} is binary, not JSON")
                raise ValueError(f"Secret {secret_name} is binary")
                
        except ClientError as e:
            logger.error(f"✗ Failed to retrieve secret {secret_name}: {e}")
            raise
    
    def get_aws_credentials(self) -> Dict[str, str]:
        """Get AWS credentials from Secrets Manager.
        
        Returns:
            Dictionary with AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        """
        return self.get_secret("aws/credentials")
    
    def get_databricks_token(self) -> str:
        """Get Databricks API token from Secrets Manager.
        
        Returns:
            Databricks API token
        """
        secret = self.get_secret("databricks/token")
        return secret.get("token", "")
    
    def get_snowflake_credentials(self) -> Dict[str, str]:
        """Get Snowflake credentials from Secrets Manager.
        
        Returns:
            Dictionary with Snowflake connection details
        """
        return self.get_secret("snowflake/credentials")
    
    @staticmethod
    def create_secret(secret_name: str, secret_value: Dict[str, str], region_name: str = "us-east-1") -> None:
        """Create a new secret in AWS Secrets Manager.
        
        Args:
            secret_name: Name of the secret
            secret_value: Dictionary with secret key-value pairs
            region_name: AWS region name
        """
        client = boto3.client("secretsmanager", region_name=region_name)
        try:
            logger.info(f"Creating secret: {secret_name}")
            client.create_secret(
                Name=secret_name,
                SecretString=json.dumps(secret_value),
                Description="Created by flight pipeline"
            )
            logger.info(f"✓ Secret created: {secret_name}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceExistsException":
                logger.warning(f"⚠ Secret {secret_name} already exists")
            else:
                logger.error(f"✗ Failed to create secret: {e}")
                raise
