"""Input and output models for /sensors_data endpoint."""

from typing import Literal, Optional

from pydantic import BaseModel, Field

SignalType = Literal["temperature", "humidity", "pressure"]
AggregatorType = Literal["avg", "max", "min"]
LocationType = Literal["office", "kitchen"]
ResolutionType = Literal["1d", "1h", "15m", None]


# INPUT
class SignalsDataInput(BaseModel):
    """Input model for aggregated signals data from sensors."""

    start_datetime: str = Field(
        example="2025-12-01T00:30:00",
        description="Start datetime for the data aggregation period",
    )
    end_datetime: str = Field(
        example="2025-12-05T00:30:00",
        description="End datetime for the data aggregation period",
    )
    resolution: ResolutionType = Field(
        example="1h",
        description="Time resolution of the aggregated data",
    )
    location: LocationType = Field(
        example="office",
        description="Location of the sensors (e.g., office, kitchen)",
    )
    signals: list[SignalType] = Field(
        example=["temperature", "pressure"],
        description="Type of signal (one of following: temperature, humidity, pressure)",  # noqa: E501
    )


# OUTPUT
class SignalsDataOutput(BaseModel):
    """Output model for aggregated signals data from sensors."""

    start_datetime: str = Field(
        example="2025-12-01T00:30:00",
        description="Start datetime for the data aggregation period",
    )
    end_datetime: str = Field(
        example="2025-12-05T00:30:00",
        description="End datetime for the data aggregation period",
    )
    resolution: ResolutionType = Field(
        example="1h",
        description="Time resolution of the aggregated data",
    )
    aggregation: AggregatorType = Field(
        example="avg",
        description="Aggregation method used (avg, max, min)",
    )
    data: Optional[list[dict[str, str | float]]] = Field(
        example=[
            {
                "ts": "2025-12-01T01:30:00Z",
                "temperature": 22.5,
                "pressure": 1013.25,
            },
            {
                "ts": "2025-12-01T02:30:00Z",
                "temperature": 23.0,
                "pressure": 1013.25,
            },
            {
                "ts": "2025-12-01T03:30:00Z",
                "temperature": 21.5,
                "pressure": 1013.25,
            },
        ],
        description="Aggregated data from sensors",
    )
