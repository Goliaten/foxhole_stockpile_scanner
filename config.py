LOG_LEVEL = "DEBUG"
LOG_DIR = "logs"

POSITION_SPEW_SLEEP_TIME = 0.05
DEFAULT_POSITION = (0, 0)
STOCKPILE_TAB_COUNT = 6
"""
Stockpiles that should be scrolled through.

Max possible amount of stockpiles visible through max is 6 (1 public + 5 reservable)
"""


LOCATIONS_DIR = "locations_files"
SOURCE_DIR = "source"
SCREENSHOT_DIR = "screenshots"
OUTPUT_DIR = "output"


SELENIUM_HEADLESS = True
FIR_PORT = 10000
"""
Port through which Foxhole Inventory Report website will be accessible.
"""
FIR_DIR = "fir_stockpile_scanner"

RECEIVER_PORT = 10001
"""
Port on which data receiver is listening for data.
"""

DISABLE_SHORTER_CSV = False
"""
Disables shortened output CSV filename, removing the risk of an overwritten output file.
"""

SLEEP_BEFORE_OPEN_MAP = 1
SLEEP_AFTER_OPEN_MAP = 1
SLEEP_AFTER_MOUSE_OVER_LOCATION = 0.4
SLEEP_BEFORE_SCREENSHOT = 0.5
"""
After you hover over a stockpile, it takes a fraction of a second to update the stockpile status.
Recommended to leave it larger than necessary.
"""
SLEEP_FILES_LEFT_TO_PROCESS_WAIT = 5
SLEEP_BEFORE_FINISHING = 10

IMAGE_EXTENSION = ".png"

LOGGER_NAME_PREFIX = "stockpile_scanner"
