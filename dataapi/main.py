from fastapi import FastAPI

from dataapi.models import SignalsDataInput, SignalsDataOutput
from dataapi.sensors_data_provider import SensorsDataProvider

app = FastAPI(title="Home Sensors Data API")


@app.post(
    "/v0/signals_data/avg",
    response_model=SignalsDataOutput,
    summary="Receive aggregated data from sensors",
    description=(
        "Endpoint to receive aggregated data (temperature, humidity, pressure) "
        "from various home sensors."
    ),
)
async def get_average(inputs: SignalsDataInput) -> SignalsDataOutput:
    output = SensorsDataProvider(
        start_datetime=inputs.start_datetime,
        end_datetime=inputs.end_datetime,
        resolution=inputs.resolution,
        location=inputs.location,
        signals=inputs.signals,
        aggregation="avg",
    ).process()

    return {
        "start_datetime": output.start_datetime,
        "end_datetime": output.end_datetime,
        "resolution": output.resolution,
        "aggregation": output.aggregation,
        "data": output.data,
    }


@app.post(
    "/v0/signals_data/max",
    response_model=SignalsDataOutput,
    summary="Receive aggregated data from sensors",
    description=(
        "Endpoint to receive aggregated data (temperature, humidity, pressure) "
        "from various home sensors."
    ),
)
async def get_maximum(inputs: SignalsDataInput) -> SignalsDataOutput:
    output = SensorsDataProvider(
        start_datetime=inputs.start_datetime,
        end_datetime=inputs.end_datetime,
        resolution=inputs.resolution,
        location=inputs.location,
        signals=inputs.signals,
        aggregation="max",
    ).process()

    return {
        "start_datetime": output.start_datetime,
        "end_datetime": output.end_datetime,
        "resolution": output.resolution,
        "aggregation": output.aggregation,
        "data": output.data,
    }
