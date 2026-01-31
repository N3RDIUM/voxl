"""This file was written by GLM 4.6 'Big Pickle' / OpenCode.

Seriously, who would waste their time writing this boring mess? I wouldn't.
"""

import glfw

# GLFW key constants mapped to human-readable names
KEYMAP = {
    # Printable keys
    "SPACE": glfw.KEY_SPACE,
    "APOSTROPHE": glfw.KEY_APOSTROPHE,  # '
    "COMMA": glfw.KEY_COMMA,  # ,
    "MINUS": glfw.KEY_MINUS,  # -
    "PERIOD": glfw.KEY_PERIOD,  # .
    "SLASH": glfw.KEY_SLASH,  # /
    # Numbers
    "KEY_0": glfw.KEY_0,
    "KEY_1": glfw.KEY_1,
    "KEY_2": glfw.KEY_2,
    "KEY_3": glfw.KEY_3,
    "KEY_4": glfw.KEY_4,
    "KEY_5": glfw.KEY_5,
    "KEY_6": glfw.KEY_6,
    "KEY_7": glfw.KEY_7,
    "KEY_8": glfw.KEY_8,
    "KEY_9": glfw.KEY_9,
    # Special characters
    "SEMICOLON": glfw.KEY_SEMICOLON,  # ;
    "EQUAL": glfw.KEY_EQUAL,  # =
    # Letters
    "A": glfw.KEY_A,
    "B": glfw.KEY_B,
    "C": glfw.KEY_C,
    "D": glfw.KEY_D,
    "E": glfw.KEY_E,
    "F": glfw.KEY_F,
    "G": glfw.KEY_G,
    "H": glfw.KEY_H,
    "I": glfw.KEY_I,
    "J": glfw.KEY_J,
    "K": glfw.KEY_K,
    "L": glfw.KEY_L,
    "M": glfw.KEY_M,
    "N": glfw.KEY_N,
    "O": glfw.KEY_O,
    "P": glfw.KEY_P,
    "Q": glfw.KEY_Q,
    "R": glfw.KEY_R,
    "S": glfw.KEY_S,
    "T": glfw.KEY_T,
    "U": glfw.KEY_U,
    "V": glfw.KEY_V,
    "W": glfw.KEY_W,
    "X": glfw.KEY_X,
    "Y": glfw.KEY_Y,
    "Z": glfw.KEY_Z,
    # Brackets and special
    "LEFT_BRACKET": glfw.KEY_LEFT_BRACKET,  # [
    "BACKSLASH": glfw.KEY_BACKSLASH,  # \
    "RIGHT_BRACKET": glfw.KEY_RIGHT_BRACKET,  # ]
    "GRAVE_ACCENT": glfw.KEY_GRAVE_ACCENT,  # `
    # World keys (non-US)
    "WORLD_1": glfw.KEY_WORLD_1,
    "WORLD_2": glfw.KEY_WORLD_2,
    # Function keys
    "ESCAPE": glfw.KEY_ESCAPE,
    "ENTER": glfw.KEY_ENTER,
    "TAB": glfw.KEY_TAB,
    "BACKSPACE": glfw.KEY_BACKSPACE,
    "INSERT": glfw.KEY_INSERT,
    "DELETE": glfw.KEY_DELETE,
    # Arrow keys
    "RIGHT": glfw.KEY_RIGHT,
    "LEFT": glfw.KEY_LEFT,
    "DOWN": glfw.KEY_DOWN,
    "UP": glfw.KEY_UP,
    # Page navigation
    "PAGE_UP": glfw.KEY_PAGE_UP,
    "PAGE_DOWN": glfw.KEY_PAGE_DOWN,
    "HOME": glfw.KEY_HOME,
    "END": glfw.KEY_END,
    # Lock keys
    "CAPS_LOCK": glfw.KEY_CAPS_LOCK,
    "SCROLL_LOCK": glfw.KEY_SCROLL_LOCK,
    "NUM_LOCK": glfw.KEY_NUM_LOCK,
    "PRINT_SCREEN": glfw.KEY_PRINT_SCREEN,
    "PAUSE": glfw.KEY_PAUSE,
    # Function keys F1-F25
    "F1": glfw.KEY_F1,
    "F2": glfw.KEY_F2,
    "F3": glfw.KEY_F3,
    "F4": glfw.KEY_F4,
    "F5": glfw.KEY_F5,
    "F6": glfw.KEY_F6,
    "F7": glfw.KEY_F7,
    "F8": glfw.KEY_F8,
    "F9": glfw.KEY_F9,
    "F10": glfw.KEY_F10,
    "F11": glfw.KEY_F11,
    "F12": glfw.KEY_F12,
    "F13": glfw.KEY_F13,
    "F14": glfw.KEY_F14,
    "F15": glfw.KEY_F15,
    "F16": glfw.KEY_F16,
    "F17": glfw.KEY_F17,
    "F18": glfw.KEY_F18,
    "F19": glfw.KEY_F19,
    "F20": glfw.KEY_F20,
    "F21": glfw.KEY_F21,
    "F22": glfw.KEY_F22,
    "F23": glfw.KEY_F23,
    "F24": glfw.KEY_F24,
    "F25": glfw.KEY_F25,
    # Keypad
    "KP_0": glfw.KEY_KP_0,
    "KP_1": glfw.KEY_KP_1,
    "KP_2": glfw.KEY_KP_2,
    "KP_3": glfw.KEY_KP_3,
    "KP_4": glfw.KEY_KP_4,
    "KP_5": glfw.KEY_KP_5,
    "KP_6": glfw.KEY_KP_6,
    "KP_7": glfw.KEY_KP_7,
    "KP_8": glfw.KEY_KP_8,
    "KP_9": glfw.KEY_KP_9,
    "KP_DECIMAL": glfw.KEY_KP_DECIMAL,
    "KP_DIVIDE": glfw.KEY_KP_DIVIDE,
    "KP_MULTIPLY": glfw.KEY_KP_MULTIPLY,
    "KP_SUBTRACT": glfw.KEY_KP_SUBTRACT,
    "KP_ADD": glfw.KEY_KP_ADD,
    "KP_ENTER": glfw.KEY_KP_ENTER,
    "KP_EQUAL": glfw.KEY_KP_EQUAL,
    # Modifiers
    "LEFT_SHIFT": glfw.KEY_LEFT_SHIFT,
    "LEFT_CONTROL": glfw.KEY_LEFT_CONTROL,
    "LEFT_ALT": glfw.KEY_LEFT_ALT,
    "LEFT_SUPER": glfw.KEY_LEFT_SUPER,
    "RIGHT_SHIFT": glfw.KEY_RIGHT_SHIFT,
    "RIGHT_CONTROL": glfw.KEY_RIGHT_CONTROL,
    "RIGHT_ALT": glfw.KEY_RIGHT_ALT,
    "RIGHT_SUPER": glfw.KEY_RIGHT_SUPER,
    "MENU": glfw.KEY_MENU,
}


def get_key_name(key_code: int):
    """Get the name of a key from its GLFW key code"""
    for name, code in KEYMAP.items():
        if code == key_code:
            return name
    return f"UNKNOWN_{key_code}"


def get_key_code(name: str):
    """Get the GLFW key code from its name"""
    return KEYMAP.get(name.upper(), None)
