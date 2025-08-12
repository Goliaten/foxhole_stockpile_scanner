from multiprocessing import Process
import os
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium import webdriver


def run_image_processor(): ...


def make_screenshot():
    print("making screenshot (not)")


def input_image(webdriver):
    img = "test_image.png"
    full_path = os.path.join(Path.cwd(), img)

    find_image_input(webdriver, full_path)


def find_image_input(webdriver: webdriver.Firefox, image_path: str):
    input_field = webdriver.find_element(By.TAG_NAME, "input")
    input_field.send_keys(image_path)
