# foxhole_stockpile_scanner

TODO
- proper readme
    - installation instructions
    - usage instructions
    - quirks / design choices
    - how to make locations file
- consider launching several FIR instances
- mitigate FIR OCR issues - reading wrong values from images

http receiver - `cd source && flask --app http_receiver run -p 10001`
core + fir - `python main.py`

# Installation
## Requirements
- Python >=3.12
- Firefox
- Unused ports 10'000, 10'001

## Downloading
To clone the project using CLI use `git clone --recurse-submodules https://github.com/Goliaten/foxhole_stockpile_scanner`.

If downloading the project directly, you'll also have to download the [submodule](https://github.com/Goliaten/fir_stockpile_scanner/tree/main), and put it in the `fir_stockpile_scanner` directory.

Packaged releases are planned.

## Installing virtual environment
### via uv
Change directory to project's root and run one of the following, depending on the OS:

<!--TODO: find better syntax highlighting-->
For Windows:
```
uv sync & .venv\Scripts\activate
```

For Linux:
```
uv sync && source .venv/bin/activate
```

### via pip
Change directory to project's root.
Then run the following commands dependin on the OS:

For Windows:
```
python -m venv .venv & .venv\Scripts\activate & python -m pip install -r requirements.txt
```

For Linux:
```
python -m venv .venv &&
source .venv\Scripts\activate &&
python -m pip install -r requirements.txt
```

# Usage
## Initial configuration
Due to script using the mouse cursor to hower over, click and write in screen, it requires a 
### params.toml
Under `[parameters]` set the following parameters in order to load correct locations file:
- `resolution` to your resolution (format is `[width, height]` in pixels)
- `scale` to your interface scale.
- `location` to hex name from which you will be executing this script.


<!-- 
1. change stuff in params.toml
1. change file in locations_files
 -->

## Launching the script.

1. Make sure you configured the script to your liking.
1. Have virtual environment with required packages active
1. Use `python main.py`


# Parametrisation.
There are 3* files that you can edit.
## 1. params.toml
## 2. config.py
## 3. One of the files in source.locations_file directory
