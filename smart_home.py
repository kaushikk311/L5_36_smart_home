import json
import os

HUB_HOST = os.getenv("SMART_HOME_HUB_HOST", "127.0.0.1")
HUB_PORT = int(os.getenv("SMART_HOME_HUB_PORT", "8080"))
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
devices = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    if settings is None:
        settings = {}
    devices[device_name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": settings,
    }


def toggle_device(device_name):
    device = devices.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return None
    device["on"] = not device["on"]
    return device["on"]


def set_temperature(device_name, value):
    device = devices.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return False
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, 16), 30)
    return True


def devices_in_room(room):
    return [
        name for name, info in devices.items()
        if info["room"] == room
    ]


def power_usage():
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)


def save_state(file_name="home_state.json"):
    with open(file_name, "w", encoding="utf-8") as state_file:
        json.dump(devices, state_file, indent=2)


def hub_address():
    return f"{HUB_HOST}:{HUB_PORT}"


def run_scene(scene_script):
    raise NotImplementedError(
    )


def main():
    """Run the smart-home demonstration."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())  # for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    active_devices = [
        name for name, info in devices.items() if info["on"]
    ]
    print("Devices on:", active_devices)
    save_state()


if __name__ == "__main__":
    main()
