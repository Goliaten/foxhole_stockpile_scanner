# foxhole_stockpile_scanner

TODO
- proper readme
    - usage instructions
    - quirks / design choices
    - how to make locations file
- consider launching several FIR instances
- mitigate FIR OCR issues - reading wrong values from images
- use FIR in the following ways:
    - scanning state of a resource field
    - scanning a bunker base
    - scanning a maintenance tunnel
    - Skynet


# Table of Content
<!-- TODO: make these points into internal links [text](link) -->
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Downloading](#downloading)
    - [Installing virtual environment](#installing-virtual-environment)
- [Usage](#usage)
    - [Initial configuration](#initial-configuration)
    - [Launching the script](#launching-the-script)
- [Parametrisation](#parametrisation)
- [Quirks / design choices](#quirks--design-choices)
- [Making locations file](#making-locations-file)


# Installation
## Requirements
- Python >=3.12
- Firefox
- Unused ports 10'000, 10'001

## Downloading
To clone the project using CLI use `git clone --recurse-submodules https://github.com/Goliaten/foxhole_stockpile_scanner`.

If downloading the project directly, you'll also have to use `git submodule update fir_stockpile_scanner` or manually download the [submodule](https://github.com/Goliaten/fir_stockpile_scanner/tree/main), and put it in the `fir_stockpile_scanner` directory.

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
This script moves your mouse on screen using pre-written co-ordinates. Unfortunately these vary depending on screen resolution and scale.
Additionally due to how in-game map search works, searching for a location from different parts of the map will pinpoint to slightly offset location. For this reason in order to load correct (or mostly correct) set of co-ordinates to work with, you have to set appropriate parameters in `params.toml`. Under `[parameters]` set the following parameters in order to load correct locations file:

- `resolution` to your resolution (format is `[width, height]` in pixels)
- `scale` to your interface scale.
- `location` to name of the hex from which you will be executing this script, or a nearby hex if location file is present for that hex. Check `./source/locations_files/` directory for matching hex name.

Script will then assemble these values into a filename to load. Format is `{resolution[0]}_{resolution[1]}_{scale}_{location}.toml`

You can see all of the available files with co-ordinates in `./source/locations_files`.
If there isn't any that matches your location, but there is one that is 1 hex away, you can safely use that one.
If there isn't any other that matches your parameters, you can make your own. Details on how to do that are be in [this chapter](#making-locations-file).
### Usage on secondary screens
In case you intend to use this script with foxhole on your secondary screen, there are additional parameters that need to be configured in `params.toml` under `[parameters]`:
- `offset_x`
- `offset_y`
- `monitor_number`

In order to set then properly, change `run_position_spew` to `true` and [launch the script](#launching-the-script).
You should see messages being written into terminal, which are the position of your mouse. First brackets shows the real value, the offset one represents value offset using the `offset_x` and `offset_y`. You should set them so that top left corner of the `offset` value on the chosen screen is at (0,0).

If values update too fast to acquire the position, you can change the refres time with `position_spew_sleep_time` parameter. Value is in seconds.

Next turn off `run_position_spew` and turn on `run_screenshot_test`. Now if you start the program, it will make a screenshot of currently chosen (based on parameters) screen, and save them to `source` (by default).

If the screen isn't correct one, you can change it using the `monitor_number` parameter. It accepts values from 0 to number of available screens.

Once you're done setting the correct screen, set `run_screenshot_test` to `false`, and the program will launch in the normal mode.

## Launching the script.

1. Make sure you configured the script to your liking.
1. Have virtual environment with required packages active
1. Use `python main.py`


# Parametrisation.
There are 3* files that you can edit.
## params.toml
- run settings
- parameters
## source/locations_file/*
## config.py
- sleep times
- subdirectory names
- fir and receiver ports(if receiver is changed, FIR js file should be changed)
- default image extension
- shorter/longer csv filenames
- FIR dirs

# Quirks / design choices
- why location files
- stockpile tab count
- stockpile tab count

# Making locations file
- explain all params and the format of position field
- turn on `run_position_spew`
- search for the field, hover mouse over target stockpile
- remember the position
- save it into the field
- repeat for every stockpile
<!-- TODO: make a guide how to create locations file -->