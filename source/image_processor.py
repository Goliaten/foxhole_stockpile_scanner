import os
from pathlib import Path
import time
from typing import Any, Dict, List
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

import source.config as cfg


def run_image_processor(params: Dict[str, Any]):
    # TODO Check if there is image to process
    # TODO if yes, put it in the website
    #   TODO wait until it's finished processing
    #   TODO click the button to send tsv
    # TODO if not, sleep
    webdriver = start_selenium()

    while True:
        images = check_for_images_to_process()
        for image in images:
            path_to_image = os.path.join(cfg.SOURCE_DIR, cfg.SCREENSHOT_DIR, image)
            input_image(webdriver, path_to_image)
            if params.get("run_settings", {}).get("neutralise_selenium"):
                time.sleep(1)
                continue

            while not is_finished(webdriver):
                time.sleep(0.1)
            click_on_tsv(webdriver)
            webdriver.refresh()

            change_name_of_screenshot(path_to_image)

        time.sleep(0.5)


def change_name_of_screenshot(image_path: str) -> None:
    path, file = os.path.split(image_path)
    os.rename(image_path, os.path.join(path, "_" + file))


def check_for_images_to_process() -> List[str]:
    return [x for x in get_dir_content() if x[-4:] == ".png" and x[0] != "_"]


def get_dir_content() -> List[str]:
    return os.listdir(os.path.join(cfg.SOURCE_DIR, cfg.SCREENSHOT_DIR))


def click_on_tsv(driver: webdriver.Remote) -> None:
    driver.find_element(By.CLASS_NAME, "tsv").click()


def is_finished(driver: webdriver.Remote) -> bool:
    # basically check if div with class=render has any children
    element = driver.find_element(By.CLASS_NAME, "render")
    child: WebElement = element.find_element(By.TAG_NAME, "img")
    if child.get_attribute("src") and child.get_attribute("src")[:4] == "data":
        return True
    return False


def start_selenium():
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(f"localhost:{cfg.FIR_PORT}")

    return driver


def input_image(driver, image_path):
    full_path = os.path.join(Path.cwd(), image_path)
    find_image_input(driver, full_path)


def find_image_input(driver: webdriver.Firefox, image_path: str):
    input_field = driver.find_element(By.TAG_NAME, "input")
    input_field.send_keys(image_path)
