import subprocess
from pynput import keyboard

keyboard_listener_thread = None


class Combination:
    def __init__(self, name, executor):
        self.name = name
        self.executor = executor


class Executor:
    def __init__(self, args, function):
        self.args = args
        self.function = function


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


# The key combinations to look for
COMBINATIONS = [
    # shift + a (see below how to get vks)
    Combination(name={get_vk(keyboard.Key.ctrl_l), get_vk(keyboard.KeyCode(vk=220))},
                executor=Executor(args="R:/cmder/Cmder.exe", function=lambda args: subprocess.check_call([args]))),
]

# The currently pressed keys (initially empty)
pressed_vks = set()


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys
    # if any(obj.name == pressed_vks for obj in COMBINATIONS):
    try:
        match_combination = next(filter(lambda combination: combination.name == pressed_vks, COMBINATIONS), None)
        if match_combination is not None:
            match_combination.executor.function(match_combination.executor.args)
    except(Exception,):
        print("there was an exception while executing macro")
        pass


def on_release(key):
    """ When a key is released """
    try:
        vk = get_vk(key)  # Get the key's vk
        pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys
    except(Exception,):
        print("there was an exception while removing keys")
        pass


def start_listener():
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()


def stop_and_join_listener():
    if keyboard_listener_thread is not None:
        keyboard_listener_thread.keyboard_listener.stop()
        keyboard_listener_thread.keyboard_listener.join()
