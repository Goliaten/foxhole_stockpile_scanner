# from multiprocessing import Process
import os
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium import webdriver


def run_image_processor(): ...


def make_screenshot():
    print("making screenshot (not)")


def input_image(driver: webdriver.Remote):
    img = "test_image.png"
    full_path = os.path.join(Path.cwd(), img)

    input_field = driver.find_element(By.TAG_NAME, "input")
    input_field.send_keys(full_path)


def get_download_button(driver: webdriver.Remote, btn_idx: int):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    # buttons = driver.find_elements_by_tag_name("button")
    buttons[btn_idx].send_keys("F:\foxhole scripts\stockpile_scanner\test")
    raise NotImplementedError


def download_as_collage():
    raise NotImplementedError


def download_as_totals():
    raise NotImplementedError


def download_as_tsv():
    raise NotImplementedError


def append_to_google_spreadsheet():
    raise NotImplementedError(
        "I'm not dealing with OAuth2 for now. NOT IMPLEMENTED ERROR"
    )
