import config

from source.core import main


def setup():
    from pathlib import Path

    Path(config.LOG_DIR).mkdir(exist_ok=True)


if __name__ == "__main__":
    setup()
    main()
