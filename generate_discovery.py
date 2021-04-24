import argparse
import copy
import json
import sys

# taken from https://raw.githubusercontent.com/merbanan/rtl_433/master/examples/rtl_433_mqtt_hass.py
MAPPINGS = {
    "temperature_C": {
        "device_type": "sensor",
        "object_suffix": "T",
        "config": {
            "device_class": "temperature",
            "name": "Temperature",
            "unit_of_measurement": "°C",
            "value_template": "{{ value|float }}"
        }
    },
    "temperature_F": {
        "device_type": "sensor",
        "object_suffix": "F",
        "config": {
            "device_class": "temperature",
            "name": "Temperature",
            "unit_of_measurement": "°F",
            "value_template": "{{ value|float }}"
        }
    },
    "battery_ok": {
        "device_type": "sensor",
        "object_suffix": "B",
        "config": {
            "device_class": "battery",
            "name": "Battery",
            "unit_of_measurement": "%",
            "value_template": "{{ float(value|int) * 99 + 1 }}"
        }
    },
    "humidity": {
        "device_type": "sensor",
        "object_suffix": "H",
        "config": {
            "device_class": "humidity",
            "name": "Humidity",
            "unit_of_measurement": "%",
            "value_template": "{{ value|float }}"
        }
    }
}


def build_json(args):
    if args.measurement_type not in MAPPINGS:
        sys.exit(f"Unknown measurement topic {args.measurement_type}")
    mapping = MAPPINGS[args.measurement_type]
    name = f"{args.device_name}-{mapping['object_suffix']}"
    configuration = copy.deepcopy(mapping["config"])
    configuration["name"] = name
    configuration["state_topic"] = args.incoming_topic
    configuration["unique_id"] = name
    configuration["device"] = {
        "identifiers": args.device_name,
        "name": args.device_name,
        "model": args.model,
        "manufacturer": args.manufacturer
    }
    # homeassistant/sensor/Acurite-Tower-A-1656/Acurite-Tower-A-1656-B/config
    return (
        f"homeassistant/{mapping['device_type']}/{args.device_name}/{name}/config",
        configuration)


def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # rtl_433/rpi/dev/AcuriteTower/1656/A/battery_ok
    parser.add_argument("--incoming_topic", type=str)
    parser.add_argument("--measurement_type", type=str)  # battery_ok
    parser.add_argument("--device_name", type=str)  # Acurite-Tower-1656-A
    parser.add_argument("--model", type=str)  # Acurite-Tower
    parser.add_argument("--manufacturer", type=str)  # rtl_433 / sensorpi
    return parser.parse_args()


def main():
    args = parse_arguments()
    info = build_json(args)
    print(info[0])
    print(json.dumps(info[1]))


if __name__ == "__main__":
    main()
