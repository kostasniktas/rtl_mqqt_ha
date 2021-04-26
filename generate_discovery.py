import argparse
import copy
import json
import sys

from mappings import MAPPINGS


# Notes
# to clear in mosquitto_pub, use -n --retain -t <TOPIC>


def build_command(format_name, topic, message):
    flags = {
        # format_name: (retain_flag, topic_flag, message_flag)
        "mosquitto_pub": ("--retain", "-t", "-m")
    }
    assert format_name in flags
    flag_map = flags[format_name]
    return " ".join([flag_map[0], flag_map[1], topic, flag_map[2], f"'{json.dumps(message)}'"])


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
    parser.add_argument("--command", type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()
    info = build_json(args)
    print()
    if args.command is None:
        print(info[0])
        print(json.dumps(info[1]))
    else:
        print(build_command(args.command, info[0], info[1]))


if __name__ == "__main__":
    main()
