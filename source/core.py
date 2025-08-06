import os
from source.mouse_manager import MM
import toml


def main() -> None:
    # get params
    cfg = toml.load(os.path.join("params.toml"))
    MM.config = cfg
    # check if game is open
    # open map
    if cfg.get("run_settings", {}).get("run_position_spew"):
        MM().spew_location()
    MM().open_map()
    # turn off all unnecessary icons
    # click on search box
    # type in location
    # navigate to seaport
    # wait for some time
    # make screenshot, click tab to go to next
    # repeat
    # parse all screenshots
    # uhh, idk, do something then
    raise NotImplementedError
