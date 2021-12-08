#!/usr/bin/env bash

if [ $# -lt 1 ]; then
  echo "Usage: $(basename $0) ACURITE_NUMBER"
  exit 1
fi

ACURITE_NUMBER=$1
ACURITE_ADJUST="$2"

CREDS_USER_FILE=".creds_sensor_user"
CREDS_PASS_FILE=".creds_sensor_pass"
MQTT_HOST=""

echo "Adding Acurite $1 with offset $2"

sudo docker run --rm -it  ruimarinho/mosquitto mosquitto_pub -h $MQTT_HOST -u "$(cat $CREDS_USER_FILE)" -P "$(cat $CREDS_PASS_FILE)" --retain -t homeassistant/sensor/Acurite-$ACURITE_NUMBER/Acurite-$ACURITE_NUMBER-T/config -m '{"device_class": "temperature", "name": "Acurite-$ACURITE_NUMBER-T", "unit_of_measurement": "\u00b0C", "value_template": "{{ (float(value) '"${2}"' ) | round(1,'floor')}}", "state_topic": "sensorpi/Acurite-Tower/'"$ACURITE_NUMBER"'/A/temperature_C", "unique_id": "Acurite-'"$ACURITE_NUMBER"'-T", "device": {"identifiers": "Acurite-'"$ACURITE_NUMBER"'", "name": "Acurite-'"$ACURITE_NUMBER"'", "model": "Acurite-Tower", "manufacturer": "sensorpi"}}'

sudo docker run --rm -it  ruimarinho/mosquitto mosquitto_pub -h $MQTT_HOST -u "$(cat $CREDS_USER_FILE)" -P "$(cat $CREDS_PASS_FILE)" --retain -t homeassistant/sensor/Acurite-$ACURITE_NUMBER/Acurite-$ACURITE_NUMBER-H/config -m '{"device_class": "humidity", "name": "Acurite-'"$ACURITE_NUMBER"'-H", "unit_of_measurement": "%", "value_template": "{{ value|float }}", "state_topic": "sensorpi/Acurite-Tower/'"$ACURITE_NUMBER"'/A/humidity", "unique_id": "Acurite-'"$ACURITE_NUMBER"'-H", "device": {"identifiers": "Acurite-'"$ACURITE_NUMBER"'", "name": "Acurite-'"$ACURITE_NUMBER"'", "model": "Acurite-Tower", "manufacturer": "sensorpi"}}'

sudo docker run --rm -it  ruimarinho/mosquitto mosquitto_pub -h $MQTT_HOST -u "$(cat $CREDS_USER_FILE)" -P "$(cat $CREDS_PASS_FILE)" --retain -t homeassistant/sensor/Acurite-$ACURITE_NUMBER/Acurite-$ACURITE_NUMBER-B/config -m '{"device_class": "battery", "name": "Acurite-'"$ACURITE_NUMBER"'-B", "unit_of_measurement": "%", "value_template": "{{ float(value|int) * 99 + 1 }}", "state_topic": "sensorpi/Acurite-Tower/'"$ACURITE_NUMBER"'/A/battery_ok", "unique_id": "Acurite-'"$ACURITE_NUMBER"'-B", "device": {"identifiers": "Acurite-'"$ACURITE_NUMBER"'", "name": "Acurite-'"$ACURITE_NUMBER"'", "model": "Acurite-Tower", "manufacturer": "sensorpi"}}'
