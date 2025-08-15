import os
from pathlib import Path
import subprocess
import time
import traceback
from typing import Any, Dict
from multiprocessing import Process
import toml

from source.image_processor import run_image_processor
from source.mouse_manager import MM
import source.config as cfg


def main() -> None:
    params = toml.load(os.path.join("params.toml"))
    fir_proc = start_fir()
    selenium_proc = start_selenium(params)
    flask_proc = start_flask()
    try:
        run_core(params)
    except BaseException:
        traceback.print_exc()
        selenium_proc.kill()
        selenium_proc.join()
        selenium_proc.close()
        fir_proc.kill()
        flask_proc.kill()


def start_selenium(params) -> Process:
    p1 = Process(target=run_image_processor, args=(params,))
    p1.start()
    return p1


def start_flask() -> subprocess.Popen:
    cmd = [
        "flask",
        "run",
        "-p",
        str(cfg.RECEIVER_PORT),
    ]
    env = os.environ.copy()
    env["FLASK_APP"] = str(
        Path.cwd() / os.path.join(cfg.SOURCE_DIR, "http_receiver.py")
    )
    p1 = subprocess.Popen(cmd, env=env)

    return p1


def start_fir() -> subprocess.Popen:
    cmd = ["python", "-m", "http.server", str(cfg.FIR_PORT), "-d", cfg.FIR_DIR]
    proc = subprocess.Popen(cmd)

    return proc


def run_core(params: Dict[str, Any]) -> None:
    # get params

    if params.get("run_settings", {}).get("neutralise_core"):
        while True:
            time.sleep(1)
            continue

    for dirr in [cfg.LOCATIONS_DIR, cfg.OUTPUT_DIR, cfg.SCREENSHOT_DIR]:
        Path(os.path.join(cfg.SOURCE_DIR, dirr)).mkdir(exist_ok=True)

    # TODO prompt user before we start for real

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
        print(f"{loc=}")
        in_game_location = MM.locations.get("locations", {})[loc]["name"]
        MM().click_search_bar()
        MM().find_location(in_game_location)
        MM().mouse_to_storage(loc)
        time.sleep(0.4)
        for cnt in range(3):
            filename = f"{round(time.time())}_{loc}_{cnt}.png"
            MM().take_screenshot(filename)
            # TODO read stockpile name
            MM().cycle_storage()
            time.sleep(0.3)
            # TODO cycle until we see the same name
        # repeat
        # uhh, idk, do something then
    time.sleep(5 * 60)
    # TODO detect that all images have been processed, then die
    raise NotImplementedError
