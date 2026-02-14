import multiprocessing
import subprocess
from typing import NotRequired, TypedDict


class ProcessDict(TypedDict):
    fir: NotRequired[subprocess.Popen]
    selenium: NotRequired[multiprocessing.Process]
    flask: NotRequired[subprocess.Popen]
