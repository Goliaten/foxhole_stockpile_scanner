from typing import Any, Dict
import pyautogui as pg
import time


class MM:
    _instance: "MM"
    config: Dict[str, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances = super(MM, cls).__call__(*args, **kwargs)
        return cls._instances

    def spew_location(self) -> None:
        while True:
            pos = pg.position()
            pos = pg.Point(
                x=pos.x + self.config.get("parameters", {}).get("offset_x", 0),
                y=pos.y + self.config.get("parameters", {}).get("offset_y", 0),
            )
            print(pos)
            time.sleep(
                self.config.get("parameters", {}).get("position_spew_sleep_time")
            )

    def open_map(self) -> None:
        raise NotImplementedError

    def click_search_bar(self) -> None:
        raise NotImplementedError

    def write_text(self, text: str) -> None:
        raise NotImplementedError

    def find_location(self, location: str) -> None:
        # click_search_bar
        # write_text
        raise NotImplementedError

    def mouse_to_storage(self, location: str) -> None:
        raise NotImplementedError

    def cycle_storage(self) -> None:
        raise NotImplementedError
