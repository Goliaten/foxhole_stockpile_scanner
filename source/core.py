import os
from pathlib import Path
import subprocess
import time
import traceback
from source.mouse_manager import MM
import toml
from selenium import webdriver

import source.config as cfg


def main() -> None:
    fir_proc = start_fir()
    selenium_proc = start_selenium()
    flask_proc = start_flask()
    try:
        run_core()
    except BaseException:
        traceback.print_exc()
        selenium_proc.close()
        fir_proc.kill()
        flask_proc.kill()


def start_flask():
    cmd = []
    p1 = subprocess.Popen(cmd)
    p1.start()

    return p1


def start_selenium():
    driver = webdriver.Firefox()
    driver.get(f"localhost:{cfg.FIR_PORT}")

    return driver


def start_fir() -> subprocess.Popen:
    cmd = ["python", "-m", "http.server", str(cfg.FIR_PORT), "-d", cfg.FIR_DIR]
    proc = subprocess.Popen(cmd)

    return proc


def run_core() -> None:
    # get params
    params = toml.load(os.path.join("params.toml"))

    for dirr in [cfg.LOCATIONS_DIR, cfg.OUTPUT_DIR, cfg.SCREENSHOT_DIR]:
        Path(os.path.join(cfg.SOURCE_DIR, dirr)).mkdir(exist_ok=True)

    MM.config = params
    MM.get_locations_file()
    # TODO check if map is open

    if params.get("run_settings", {}).get("run_position_spew"):
        MM().spew_location()
    if params.get("run_settings", {}).get("click_on_position_at_start"):
        MM().click(
            params.get("run_settings", {}).get("position_to_click_at_start", (0, 0))
        )
    time.sleep(1)
    MM().open_map()
    time.sleep(1)
    # TODO turn off all unnecessary icons

    for loc in MM.locations.get("locations", {}).keys():
        MM().click_search_bar()
        MM().find_location(loc)
        MM().mouse_to_storage(loc)
        time.sleep(0.4)
        for cnt in range(3):
            filename = f"{round(time.time())}_{loc}_{cnt}.png"
            MM().take_screenshot(filename)
            # TODO read stockpile name
            MM().cycle_storage()
            time.sleep(0.3)
            # TODO parse screenshot in selenium
            # TODO cycle until we see the same name
        # repeat
        # uhh, idk, do something then
        raise NotImplementedError
