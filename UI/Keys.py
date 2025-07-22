import pygame
from Event.EventHandler import *
import Utility.Temporal as Temporal
import pygame

class PLT_KeyData:
    def __init__(self):
        self.Down                   : bool  = False

        self.DownDuration           : float = -1.0
        self.DownDurationPrev       : float = -1.0

        self.Pressed                : bool  = False
        self.Released               : bool  = False

        self.AnalogValue            : float = 0.0

        self.Keycode                : int   = -1

KEY_MAP = {'0': 48,
 '1': 49,
 '2': 50,
 '3': 51,
 '4': 52,
 '5': 53,
 '6': 54,
 '7': 55,
 '8': 56,
 '9': 57,
 'AC_BACK': 1073742094,
 'AMPERSAND': 38,
 'ASTERISK': 42,
 'AT': 64,
 'BACKQUOTE': 96,
 'BACKSLASH': 92,
 'BACKSPACE': 8,
 'BREAK': 1073741896,
 'CAPSLOCK': 1073741881,
 'CARET': 94,
 'CLEAR': 1073741980,
 'COLON': 58,
 'COMMA': 44,
 'CURRENCYSUBUNIT': 1073742005,
 'CURRENCYUNIT': 1073742004,
 'DELETE': 127,
 'DOLLAR': 36,
 'DOWN': 1073741905,
 'END': 1073741901,
 'EQUALS': 61,
 'ESCAPE': 27,
 'EURO': 1073742004,
 'EXCLAIM': 33,
 'F1': 1073741882,
 'F10': 1073741891,
 'F11': 1073741892,
 'F12': 1073741893,
 'F13': 1073741928,
 'F14': 1073741929,
 'F15': 1073741930,
 'F2': 1073741883,
 'F3': 1073741884,
 'F4': 1073741885,
 'F5': 1073741886,
 'F6': 1073741887,
 'F7': 1073741888,
 'F8': 1073741889,
 'F9': 1073741890,
 'GREATER': 62,
 'HASH': 35,
 'HELP': 1073741941,
 'HOME': 1073741898,
 'INSERT': 1073741897,
 'KP0': 1073741922,
 'KP1': 1073741913,
 'KP2': 1073741914,
 'KP3': 1073741915,
 'KP4': 1073741916,
 'KP5': 1073741917,
 'KP6': 1073741918,
 'KP7': 1073741919,
 'KP8': 1073741920,
 'KP9': 1073741921,
 'KP_0': 1073741922,
 'KP_1': 1073741913,
 'KP_2': 1073741914,
 'KP_3': 1073741915,
 'KP_4': 1073741916,
 'KP_5': 1073741917,
 'KP_6': 1073741918,
 'KP_7': 1073741919,
 'KP_8': 1073741920,
 'KP_9': 1073741921,
 'KP_DIVIDE': 1073741908,
 'KP_ENTER': 1073741912,
 'KP_EQUALS': 1073741927,
 'KP_MINUS': 1073741910,
 'KP_MULTIPLY': 1073741909,
 'KP_PERIOD': 1073741923,
 'KP_PLUS': 1073741911,
 'LALT': 1073742050,
 'LCTRL': 1073742048,
 'LEFT': 1073741904,
 'LEFTBRACKET': 91,
 'LEFTPAREN': 40,
 'LESS': 60,
 'LGUI': 1073742051,
 'LMETA': 1073742051,
 'LSHIFT': 1073742049,
 'LSUPER': 1073742051,
 'MENU': 1073741942,
 'MINUS': 45,
 'MODE': 1073742081,
 'NUMLOCK': 1073741907,
 'NUMLOCKCLEAR': 1073741907,
 'PAGEDOWN': 1073741902,
 'PAGEUP': 1073741899,
 'PAUSE': 1073741896,
 'PERCENT': 37,
 'PERIOD': 46,
 'PLUS': 43,
 'POWER': 1073741926,
 'PRINT': 1073741894,
 'PRINTSCREEN': 1073741894,
 'QUESTION': 63,
 'QUOTE': 39,
 'QUOTEDBL': 34,
 'RALT': 1073742054,
 'RCTRL': 1073742052,
 'RETURN': 13,
 'RGUI': 1073742055,
 'RIGHT': 1073741903,
 'RIGHTBRACKET': 93,
 'RIGHTPAREN': 41,
 'RMETA': 1073742055,
 'RSHIFT': 1073742053,
 'RSUPER': 1073742055,
 'SCROLLLOCK': 1073741895,
 'SCROLLOCK': 1073741895,
 'SEMICOLON': 59,
 'SLASH': 47,
 'SPACE': 32,
 'SYSREQ': 1073741978,
 'TAB': 9,
 'UNDERSCORE': 95,
 'UNKNOWN': 0,
 'UP': 1073741906,
 'a': 97,
 'b': 98,
 'c': 99,
 'd': 100,
 'e': 101,
 'f': 102,
 'g': 103,
 'h': 104,
 'i': 105,
 'j': 106,
 'k': 107,
 'l': 108,
 'm': 109,
 'n': 110,
 'o': 111,
 'p': 112,
 'q': 113,
 'r': 114,
 's': 115,
 't': 116,
 'u': 117,
 'v': 118,
 'w': 119,
 'x': 120,
 'y': 121,
 'z': 122}

_KeysInitState = {0: PLT_KeyData(),
 8: PLT_KeyData(),
 9: PLT_KeyData(),
 13: PLT_KeyData(),
 27: PLT_KeyData(),
 32: PLT_KeyData(),
 33: PLT_KeyData(),
 34: PLT_KeyData(),
 35: PLT_KeyData(),
 36: PLT_KeyData(),
 37: PLT_KeyData(),
 38: PLT_KeyData(),
 39: PLT_KeyData(),
 40: PLT_KeyData(),
 41: PLT_KeyData(),
 42: PLT_KeyData(),
 43: PLT_KeyData(),
 44: PLT_KeyData(),
 45: PLT_KeyData(),
 46: PLT_KeyData(),
 47: PLT_KeyData(),
 48: PLT_KeyData(),
 49: PLT_KeyData(),
 50: PLT_KeyData(),
 51: PLT_KeyData(),
 52: PLT_KeyData(),
 53: PLT_KeyData(),
 54: PLT_KeyData(),
 55: PLT_KeyData(),
 56: PLT_KeyData(),
 57: PLT_KeyData(),
 58: PLT_KeyData(),
 59: PLT_KeyData(),
 60: PLT_KeyData(),
 61: PLT_KeyData(),
 62: PLT_KeyData(),
 63: PLT_KeyData(),
 64: PLT_KeyData(),
 91: PLT_KeyData(),
 92: PLT_KeyData(),
 93: PLT_KeyData(),
 94: PLT_KeyData(),
 95: PLT_KeyData(),
 96: PLT_KeyData(),
 97: PLT_KeyData(),
 98: PLT_KeyData(),
 99: PLT_KeyData(),
 100: PLT_KeyData(),
 101: PLT_KeyData(),
 102: PLT_KeyData(),
 103: PLT_KeyData(),
 104: PLT_KeyData(),
 105: PLT_KeyData(),
 106: PLT_KeyData(),
 107: PLT_KeyData(),
 108: PLT_KeyData(),
 109: PLT_KeyData(),
 110: PLT_KeyData(),
 111: PLT_KeyData(),
 112: PLT_KeyData(),
 113: PLT_KeyData(),
 114: PLT_KeyData(),
 115: PLT_KeyData(),
 116: PLT_KeyData(),
 117: PLT_KeyData(),
 118: PLT_KeyData(),
 119: PLT_KeyData(),
 120: PLT_KeyData(),
 121: PLT_KeyData(),
 122: PLT_KeyData(),
 127: PLT_KeyData(),
 1073741881: PLT_KeyData(),
 1073741882: PLT_KeyData(),
 1073741883: PLT_KeyData(),
 1073741884: PLT_KeyData(),
 1073741885: PLT_KeyData(),
 1073741886: PLT_KeyData(),
 1073741887: PLT_KeyData(),
 1073741888: PLT_KeyData(),
 1073741889: PLT_KeyData(),
 1073741890: PLT_KeyData(),
 1073741891: PLT_KeyData(),
 1073741892: PLT_KeyData(),
 1073741893: PLT_KeyData(),
 1073741894: PLT_KeyData(),
 1073741895: PLT_KeyData(),
 1073741896: PLT_KeyData(),
 1073741897: PLT_KeyData(),
 1073741898: PLT_KeyData(),
 1073741899: PLT_KeyData(),
 1073741901: PLT_KeyData(),
 1073741902: PLT_KeyData(),
 1073741903: PLT_KeyData(),
 1073741904: PLT_KeyData(),
 1073741905: PLT_KeyData(),
 1073741906: PLT_KeyData(),
 1073741907: PLT_KeyData(),
 1073741908: PLT_KeyData(),
 1073741909: PLT_KeyData(),
 1073741910: PLT_KeyData(),
 1073741911: PLT_KeyData(),
 1073741912: PLT_KeyData(),
 1073741913: PLT_KeyData(),
 1073741914: PLT_KeyData(),
 1073741915: PLT_KeyData(),
 1073741916: PLT_KeyData(),
 1073741917: PLT_KeyData(),
 1073741918: PLT_KeyData(),
 1073741919: PLT_KeyData(),
 1073741920: PLT_KeyData(),
 1073741921: PLT_KeyData(),
 1073741922: PLT_KeyData(),
 1073741923: PLT_KeyData(),
 1073741926: PLT_KeyData(),
 1073741927: PLT_KeyData(),
 1073741928: PLT_KeyData(),
 1073741929: PLT_KeyData(),
 1073741930: PLT_KeyData(),
 1073741941: PLT_KeyData(),
 1073741942: PLT_KeyData(),
 1073741978: PLT_KeyData(),
 1073741980: PLT_KeyData(),
 1073742004: PLT_KeyData(),
 1073742005: PLT_KeyData(),
 1073742048: PLT_KeyData(),
 1073742049: PLT_KeyData(),
 1073742050: PLT_KeyData(),
 1073742051: PLT_KeyData(),
 1073742052: PLT_KeyData(),
 1073742053: PLT_KeyData(),
 1073742054: PLT_KeyData(),
 1073742055: PLT_KeyData(),
 1073742081: PLT_KeyData(),
 1073742094: PLT_KeyData()}


class Keys:
    _KEYS : dict[int , PLT_KeyData] = {}

    @staticmethod
    def GetKey(keycode : int) -> PLT_KeyData:
        return Keys._KEYS[keycode]

    @staticmethod
    def IsKeyDown(keycode : int) -> bool:
        """if the key is down"""
        return Keys._KEYS[keycode].Down

    @staticmethod
    def IsKeyPressed(keycode : int) -> bool:
        """if the key was pressed on that frame"""
        return Keys._KEYS[keycode].Pressed

    @staticmethod
    def IsKeyReleased(keycode : int) -> bool:
        """if the key was released on that frame"""
        return Keys._KEYS[keycode].Released
    
    @staticmethod
    def Update():
        for key in Keys._KEYS.values():
            key.Pressed     = key.Down and key.DownDuration < 0.0
            key.Released    = (not key.Down) and key.DownDuration >= 0.0
            key.DownDurationPrev = key.DownDuration

            if key.Down:
                if key.DownDuration < 0.0:  key.DownDuration = 0.0
                else:  key.DownDuration += Temporal.PlotEngineTime.DeltaTime()
            else:
                key.DownDuration = -1.0

    @staticmethod
    def _OnEvent(event : Event):
        if event.GetName() == "KeyDown":
            Keys._KEYS[event.keycode].Down = True
            Keys._KEYS[event.keycode].Keycode = event.keycode

            print(f"key pressed : {event.keycode}")

        if event.GetName() == "KeyUp":
            Keys._KEYS[event.keycode].Down = False

    @classmethod
    def Init(cls):
        cls._KEYS = _KeysInitState
        AddEventListener(cls._OnEvent)
