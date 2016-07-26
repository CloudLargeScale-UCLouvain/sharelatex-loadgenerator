
## Example usage:

environment variables:

- LOCUST\_DURATION
- LOCUST\_HATCH\_RATE
- LOCUST\_INFLUXDB\_SERVER
- LOCUST\_INFLUXDB\_PORT
- LOCUST\_INFLUXDB\_USER
- LOCUST\_INFLUXDB\_PASSWORD
- LOCUST\_INFLUXDB\_DB
- LOCUST\_LOAD\_TYPE
- LOCUST\_METRICS\_EXPORT
- LOCUST\_MEASUREMENT\_NAME
- LOCUST\_MEASUREMENT\_DESCRIPTION
- LOCUST\_STATSD\_HOST
- LOCUST\_STATSD\_PORT
- LOCUST\_SPAWN\_WAIT\_MEAN
- LOCUST\_SPAWN\_WAIT\_STD
- LOCUST\_USERS
- LOCUST\_USER\_MEAN
- LOCUST\_USER\_STD
- LOCUST\_WAIT\_MEAN
- LOCUST\_WAIT\_STD

```
$ export LOCUST_STATSD_HOST=172.17.0.7 \
    LOCUST_DURATION=360 \
    LOCUST_USERS=10 \
    LOCUST_WAIT_MEAN=10 \
    LOCUST_WAIT_STD=4 \
    LOCUST_METRICS_EXPORT="measurements" \
    LOCUST_MEASUREMENT_NAME="measurement" \
    LOCUST_MEASUREMENT_DESCRIPTION="linear increase" \
    LOCUST_INFLUXDB_SERVER="influxdb.local" \
    LOCUST_INFLUXDB_PORT="8086" \
    LOCUST_INFLUXDB_USER="influxdb" \
    LOCUST_INFLUXDB_PASSWORD="rewtrewt" \
    LOCUST_INFLUXDB_DB="metrics"
$ locust -H http://sharelatex.local
```
