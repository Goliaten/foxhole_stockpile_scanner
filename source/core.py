import os
import subprocess
import time
import traceback
from source.mouse_manager import MM
import toml
from selenium import webdriver

from source.image_processor import get_download_button, input_image, make_screenshot
import source.config as cfg


def main() -> None:
    fir_proc = start_fir()
    selenium_proc = start_selenium()
    try:
        input_image(selenium_proc)
        time.sleep(5)
        # get_download_button(selenium_proc, 1)
        while True:
            time.sleep(2)
        # run_core()
    except BaseException:
        traceback.print_exc()
        murder_process(fir_proc)
        selenium_proc.close()


def murder_process(proc: subprocess.Popen) -> None:
    proc.kill()


def start_selenium() -> webdriver.Remote:
    driver = webdriver.Firefox()
    driver.get(f"localhost:{cfg.FIR_PORT}")

    return driver


def start_fir() -> subprocess.Popen:
    cmd = ["python", "-m", "http.server", str(cfg.FIR_PORT), "-d", "fir"]
    proc = subprocess.Popen(cmd)

    return proc


def run_core() -> None:
    # get params
    cfg = toml.load(os.path.join("params.toml"))
    MM.config = cfg
    MM.get_locations_file()
    # TODO check if map is open

    if cfg.get("run_settings", {}).get("run_position_spew"):
        MM().spew_location()
    if cfg.get("run_settings", {}).get("click_on_position_at_start"):
        MM().click(
            cfg.get("run_settings", {}).get("position_to_click_at_start", (0, 0))
        )
    time.sleep(1)
    MM().open_map()
    time.sleep(0.1)
    # TODO turn off all unnecessary icons

    for loc in MM.locations.get("locations", {}).keys():
        MM().click_search_bar()
        MM().find_location(loc)
        MM().mouse_to_storage(loc)
        time.sleep(0.4)
        for x in range(3):
            make_screenshot()
            MM().cycle_storage()
            time.sleep(0.3)
        # TODO parse screenshot
        # TODO read name
        # TODO cycle until we see the same name
        # repeat
        # uhh, idk, do something then
        raise NotImplementedError
