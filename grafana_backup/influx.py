import datetime
import influxdb
import sys


def main(args, settings):
    influxdb_measurement = settings.get('INFLUXDB_MEASUREMENT')
    influxdb_host = settings.get('INFLUXDB_HOST')
    influxdb_port = settings.get('INFLUXDB_PORT')
    influxdb_username = settings.get('INFLUXDB_USERNAME')
    influxdb_password = settings.get('INFLUXDB_PASSWORD')
    influxdb_database = settings.get('INFLUXDB_DATABASE')

    # write stats to InfluxDB
    influx = influxdb.InfluxDBClient(
        host=influxdb_host,
        port=influxdb_port,
        username=influxdb_username,
        password=influxdb_password,
        database=influxdb_database,
        ssl=False,
        verify_ssl=False
    )

    try:
        result = influx.write_points([{
            "measurement": influxdb_measurement,
            "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "fields": {
                "backed_up": True
            }
        }])
        if result is True:
            print("InfluxDB metrics written successfully.")
    except Exception as e:
        print('InfluxDB exception: \n{0}'.format(str(e)))
        sys.exit(1)

    return True
