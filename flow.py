from phue import Bridge
from prefect import task, flow

modes = {
    'main': {
        'kitchen': 'Arctic aurora',
        'office': 'Blood moon',
        'living room': 'sahara',
        'bedroom': 'Nightlight'
    },
    'clean': {
        'kitchen': 'Bright',
        'office': 'Bright',
        'living room': 'Bright',
        'bedroom': 'Bright'
    },
    'morning': {
        'kitchen': 'Ocean dawn',
        'office': 'Tropical twilight',
        'living room': 'monet',
        'bedroom': 'Relax'
    }
}

@task
def update_group_lights(
    bridge: Bridge,
    group_name: str,
    scene_name: str,
    transition: int = 100 # 100 * 0.1 second
) -> bool:
            
    print(f'Setting {group_name} to {scene_name}')
    
    return bridge.run_scene(
        group_name=group_name,
        scene_name=scene_name,
        transition_time=transition
    )

@flow
def smart_home(choice: str) -> None:
        
    bridge = Bridge()

    mode = modes[choice]

    for group_name, scene_name in mode.items():
        try:
            assert update_group_lights(bridge, group_name, scene_name)
        
        except AssertionError:
            print(f'Failed to run scene in {group_name}')
            raise

if __name__ == "__main__":
    smart_home('main')
    
