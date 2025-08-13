import os
from typing import Any, Dict, Tuple
import mss
import pyautogui as pg  # type: ignore
import time

import toml
import source.config as cfg


class MM:
    _instance: "MM"
    config: Dict[str, Any] = {}
    locations: Dict[str, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances = super(MM, cls).__call__(*args, **kwargs)
        return cls._instances

    @classmethod
    def get_locations_file(cls):
        params = cls.config.get("parameters", {})
        res_x = params.get("resolution")[0]
        res_y = params.get("resolution")[1]
        scale = params.get("scale")

        file = f"{res_x}_{res_y}_{scale}.toml"
        path = os.path.join(cfg.SOURCE_DIR, cfg.LOCATIONS_DIR, file)

        if os.path.exists(path):
            print("Loaded")
            cls.locations = toml.load(path)
        else:
            msg = f"Cannot find {path}"
            raise FileNotFoundError(msg)

    def spew_location(self) -> None:
        while True:
            pos = pg.position()
            pos = (pos.x, pos.y)
            print(f"Position: {pos}, offset: {self.offset_point(pos, True)}")
            time.sleep(cfg.POSITION_SPEW_SLEEP_TIME)

    def offset_point(self, pos: Tuple[int, int], reverse=False) -> Tuple[int, int]:
        off_x = self.config.get("parameters", {}).get("offset_x", 0)
        off_y = self.config.get("parameters", {}).get("offset_y", 0)
        if reverse:
            return pos[0] - off_x, pos[1] - off_y
        return pos[0] + off_x, pos[1] + off_y

    def click(self, pos: Tuple[int, int], offset=True):
        if offset:
            pos = self.offset_point(pos)
        pg.click(*pos)

    def mouse_to(self, pos: Tuple[int, int], offset=True):
        if offset:
            pos = self.offset_point(pos)
        pg.moveTo(*pos)

    def open_map(self) -> None:
        pg.typewrite(["M"])

    def click_search_bar(self) -> None:
        pos = self.locations.get("search_bar", cfg.DEFAULT_POSITION)

        self.click(pos)

    def clean_text(self, times=4) -> None:
        for x in range(times):
            pg.hotkey("ctrl", "backspace")

    def write_text(self, text: str, enter=False) -> None:
        pg.typewrite(message=text, interval=0.02)

    def click_first_result(self) -> None:
        pos = self.locations.get("first_search_position", cfg.DEFAULT_POSITION)
        self.click(pos)

    def find_location(self, location: str) -> None:
        # write_text
        self.clean_text()
        self.write_text(location)
        self.click_first_result()

    def mouse_to_storage(self, location: str) -> None:
        pos = self.locations.get("locations", {}).get(location)
        print(f"Position(storage): {pos}")
        self.mouse_to(pos)

    def cycle_storage(self) -> None:
        pg.typewrite(["tab"])

    def take_screenshot(self, filename: str) -> None:
        path = os.path.join(cfg.SOURCE_DIR, cfg.SCREENSHOT_DIR, filename)
        with mss.mss() as sct:
            mon = sct.monitors[
                self.config.get("parameters", {}).get("monitor_number", 1)
            ]
            sct_img = sct.grab(mon)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=path)
