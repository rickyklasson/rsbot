"""Autoclicker which records keystrokes and repeats actions"""
import argparse
import time
from utils import window_util, input_util

def main(args):
    # Wait for user acknowledgement.
    input('Press ENTER to start recording. Then x to stop recording once finished.')

    # Find window of interest.
    win = window_util.find_window(args.window)
    
    # Bring it into focus.
    win.minimize()
    win.restore()

    # Record mouse inputs.
    raw_input = input_util.record_mouse_input()

    # Filter mouse inputs.
    filt_inputs = input_util.filter_clicks(raw_input)

    # Wait for user confirmation.
    print('Waiting for 5s delay before replaying input.')
    time.sleep(5)

    # Replay input.
    input_util.replay_inputs(filt_inputs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('\n\nRun command example:\npython autoclicker.py --window RuneLite')
    
    # Required positional argument
    #parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    #parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-w", "--window", action="store", dest="window", type=str)

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    #parser.add_argument(
    #    "-v",
    #    "--verbose",
    #    action="count",
    #    default=0,
    #    help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    #parser.add_argument(
    #    "--version",
    #    action="version",
    #    version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)