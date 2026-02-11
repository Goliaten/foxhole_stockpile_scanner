import os
from pathlib import Path
import subprocess
import time
import traceback
from typing import Any, Dict
from multiprocessing import Process
import toml

from source.helpers.printout_helper import in_out_wrapper
from source.image_processor import check_for_images_to_process, run_image_processor
from source.mouse_manager import MM
import config as cfg


def main() -> None:
    params = toml.load(os.path.join("params.toml"))
    # TODO don't start these subprocesses if we run position spew or screenshot check
    fir_proc = start_fir()
    selenium_proc = start_selenium(params)
    flask_proc = start_flask()

    try:
        run_core(params)
    except SystemExit:
        pass
    except BaseException:
        traceback.print_exc()

    kill_child_processes(selenium_proc, fir_proc, flask_proc)


def kill_child_processes(
    selenium_proc: Process, fir_proc: subprocess.Popen, flask_proc: subprocess.Popen
):
    selenium_proc.kill()
    selenium_proc.join()
    selenium_proc.close()
    fir_proc.kill()
    flask_proc.kill()


@in_out_wrapper
def start_selenium(params) -> Process:
    p1 = Process(target=run_image_processor, args=(params,))
    p1.start()
    return p1


@in_out_wrapper
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


@in_out_wrapper
def start_fir() -> subprocess.Popen:
    cmd = ["python", "-m", "http.server", str(cfg.FIR_PORT), "-d", cfg.FIR_DIR]
    proc = subprocess.Popen(cmd)

    return proc


@in_out_wrapper
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

    if params.get("run_settings", {}).get("run_screenshot_test"):
        MM().take_screenshot()
        exit()
    if params.get("run_settings", {}).get("run_position_spew"):
        MM().spew_location()
        exit()
    if params.get("run_settings", {}).get("click_on_position_at_start"):
        MM().click(
            params.get("run_settings", {}).get("position_to_click_at_start", (0, 0))
        )
    time.sleep(cfg.SLEEP_BEFORE_OPEN_MAP)
    MM().open_map()
    time.sleep(cfg.SLEEP_AFTER_OPEN_MAP)
    # TODO turn off all unnecessary icons

    for loc in MM.locations.get("locations", {}).keys():
        in_game_location = MM.locations.get("locations", {})[loc]["name"]

        print(
            f"Key: {loc}; "
            f"Location: {in_game_location}; "
            f"Position: {MM.locations.get('locations', {})[loc]}"
        )

        MM().click_search_bar()
        MM().find_location(in_game_location)
        MM().mouse_to_storage(loc)

        time.sleep(cfg.SLEEP_AFTER_MOUSE_OVER_LOCATION)

        # TODO make something better than looping over all stockpiles X times
        for cnt in range(cfg.STOCKPILE_TAB_COUNT):
            filename = f"{round(time.time())}_{loc}_{cnt}{cfg.IMAGE_EXTENSION}"

            time.sleep(cfg.SLEEP_BEFORE_SCREENSHOT)
            MM().take_screenshot(filename)
            MM().cycle_storage()

    print("Finished making screenshots.")

    while check_for_images_to_process():
        print(
            "Images still processing. "
            f"Sleeping for {cfg.SLEEP_FILES_LEFT_TO_PROCESS_WAIT} seconds"
        )
        time.sleep(cfg.SLEEP_FILES_LEFT_TO_PROCESS_WAIT)

    print(
        "Finished sending images to FIR. "
        f"Will exit in {cfg.SLEEP_BEFORE_FINISHING} seconds."
    )
    time.sleep(cfg.SLEEP_BEFORE_FINISHING)
