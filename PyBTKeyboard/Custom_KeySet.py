import json

from pynput.keyboard import Key, Controller


class Custom_KeySet:
    def __init__(self):
        self._controller = Controller()
        self._keyDict = {
            "Key.alt": Key.alt,
            "Key.alt_l": Key.alt_l,
            "Key.alt_r": Key.alt_r,
            "Key.alt_gr": Key.alt_gr,
            "Key.backspace": Key.backspace,
            "Key.caps_lock": Key.caps_lock,
            "Key.cmd": Key.cmd,
            "Key.cmd_l": Key.cmd_l,
            "Key.cmd_r": Key.cmd_r,
            "Key.ctrl": Key.ctrl,
            "Key.ctrl_l": Key.ctrl_l,
            "Key.ctrl_r": Key.ctrl_r,
            "Key.delete": Key.delete,
            "Key.down": Key.down,
            "Key.end": Key.end,
            "Key.enter": Key.enter,
            "Key.esc": Key.esc,
            "Key.f1": Key.f1,
            "Key.f2": Key.f2,
            "Key.f3": Key.f3,
            "Key.f4": Key.f4,
            "Key.f5": Key.f5,
            "Key.f6": Key.f6,
            "Key.f7": Key.f7,
            "Key.f8": Key.f8,
            "Key.f9": Key.f9,
            "Key.f10": Key.f10,
            "Key.f11": Key.f11,
            "Key.f12": Key.f12,
            "Key.f13": Key.f13,
            "Key.f14": Key.f14,
            "Key.f15": Key.f15,
            "Key.f16": Key.f16,
            "Key.f17": Key.f17,
            "Key.f18": Key.f18,
            "Key.f19": Key.f19,
            "Key.f20": Key.f20,
            "Key.home": Key.home,
            "Key.left": Key.left,
            "Key.page_down": Key.page_down,
            "Key.page_up": Key.page_up,
            "Key.right": Key.right,
            "Key.shift": Key.shift,
            "Key.shift_l": Key.shift_l,
            "Key.shift_r": Key.shift_r,
            "Key.space": Key.space,
            "Key.tab": Key.tab,
            "Key.up": Key.up,
            "Key.media_play_pause": Key.media_play_pause,
            "Key.media_volume_mute": Key.media_volume_mute,
            "Key.media_volume_down": Key.media_volume_down,
            "Key.media_volume_up": Key.media_volume_up,
            "Key.media_previous": Key.media_previous,
            "Key.media_next": Key.media_next,
            "Key.insert": Key.insert,
            "Key.menu": Key.menu,
            "Key.num_lock": Key.num_lock,
            "Key.pause": Key.pause,
            "Key.print_screen": Key.print_screen,
            "Key.scroll_lock": Key.scroll_lock,
        }
        with open("user_key.json", "r") as file:
            self.userKeys = json.load(file)

    def inputKey(self, key):
        if key in self.userKeys.keys():
            print(f"Received BT data: {key} -> {self.userKeys[key]}")
            if self.userKeys[key] in self._keyDict.keys():
                self._controller.tap(self._keyDict[self.userKeys[key]])
            else:
                raise KeyError("The key dosen't exist in keyDict")
        else:
            raise KeyError("The input key dosen't exist in json file")