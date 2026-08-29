"""Type definitions and data models for flight pipeline."""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class FlightData:
    """Represents a single flight record from OpenSky API."""
    
    icao24: str
    """ICAO 24-bit address of the aircraft."""
    
    callsign: Optional[str]
    """Callsign of the aircraft."""
    
    origin_country: str
    """Country of origin."""
    
    longitude: float
    """Longitude coordinate."""
    
    latitude: float
    """Latitude coordinate."""
    
    altitude_meters: Optional[float]
    """Altitude in meters (barometric)."""
    
    velocity_ms: Optional[float]
    """Velocity in meters per second."""
    
    ingested_at: datetime
    """Timestamp when data was ingested."""


@dataclass
class APIResponse:
    """OpenSky Network API response."""
    
    time: int
    """Unix timestamp."""
    
    states: List[List[Any]]
    """List of flight state vectors."""


@dataclass
class IngestionResult:
    """Result of data ingestion operation."""
    
    success: bool
    """Whether ingestion was successful."""
    
    records_processed: int
    """Number of records processed."""
    
    s3_path: str
    """S3 path where data was uploaded."""
    
    timestamp: datetime
    """Timestamp of ingestion."""
    
    error_message: Optional[str] = None
    """Error message if ingestion failed."""
