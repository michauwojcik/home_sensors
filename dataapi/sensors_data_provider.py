import os

from influxdb_client import InfluxDBClient

from dataapi.models.sensor_data import SignalsDataOutput

INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST")
INFLUXDB_PORT = os.environ.get("INFLUXDB_PORT")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")


class SensorsDataProvider:
    BUCKET = os.environ.get("INFLUXDB_BUCKET")

    """Provider for data from BME280 sensors."""

    def __init__(
        self,
        start_datetime: str,
        end_datetime: str,
        resolution: str,
        location: str,
        signals: list[str],
        aggregation: str,
    ):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.resolution = resolution
        self.location = location
        self.signals = signals
        self.aggregation = aggregation

    @property
    def influx_client(self) -> InfluxDBClient:
        """Create and return an InfluxDB client."""
        return InfluxDBClient(
            url=f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}",
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG,
        )

    def process(self):
        # Placeholder implementation for demonstration purposes
        query = self._prepare_query(
            start_timestamp=self.start_datetime,
            stop_timestamp=self.end_datetime,
        )
        tables = self.influx_client.query_api().query(query)

        # Group records by timestamp and aggregate them
        # Structure: {timestamp: {signal_name: value}}
        timestamp_data = {}
        for table in tables:
            for record in table.records:
                ts = record.get_time().isoformat()
                signal_name = record.get_field()
                value = record.get_value()

                if ts not in timestamp_data:
                    timestamp_data[ts] = {}
                timestamp_data[ts][signal_name] = value

        output_data = [
            {"ts": ts, **signals} for ts, signals in sorted(timestamp_data.items())
        ]

        return SignalsDataOutput(
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            resolution=self.resolution,
            aggregation=self.aggregation,
            data=output_data,
        )

    def _prepare_query(
        self,
        start_timestamp: str = "-1h",
        stop_timestamp: str = "now()",
        window: str = "1h",
    ) -> str:
        _field_condition = " or ".join(
            [f'r["_field"] == "{signal}"' for signal in self.signals]
        )

        aggregation_function = {
            "avg": "mean",
            "max": "max",
        }.get(self.aggregation, "mean")

        # TODO:
        # convert start_timestamp and stop_timestamp to UTC ISO 8601 format
        return f"""
            from(bucket: "temp_humidity_pressure")
            |> range(start: time(v: "{start_timestamp}Z"), stop: time(v: "{stop_timestamp}Z"))
            |> filter(fn: (r) => r._measurement == "bme280_signals")
            |> filter(fn: (r) => {_field_condition})
            |> filter(fn: (r) => r.location == "{self.location}")
            |> aggregateWindow(every: {window}, fn: {aggregation_function}, createEmpty: false)
        """  # noqa: E501
