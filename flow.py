from difflib import get_close_matches
from phue import Bridge
from prefect import task, flow
from time import sleep
from typing import Any, Union

def connect() -> Bridge:
    PHILLIPS_HUE_BRIDGE_IP = '192.168.0.165'

    return Bridge(PHILLIPS_HUE_BRIDGE_IP)


def handle(status: Any):
    match status[0][0]:
        case {'error': error}:
            print(f"{error['type']} ERROR: {error['description']}")
            match error['description']:
                case 'Device is set to off':
                    print('wow this is cool')

@task(name="Toggle some lights")
def toggle(room: str, brightness: Union[int, dict]) -> None:
    bridge = connect()

    room_names = {j['name']: i for i, j in bridge.get_group().items()}

    room_number = room_names[get_close_matches(room, room_names.keys())[0]]

    lights = bridge.get_group(int(room_number), 'lights')

    for light_id in lights:
        config = {
            'bri': brightness
        }

        status = bridge.set_light(int(light_id), config)

        handle(status)



        

@flow
def smart_home():

    room = 'kitchen'
    brightness = 150

    toggle(room, brightness)

if __name__ == "__main__":
    smart_home()