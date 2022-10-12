"""Autoclicker which records keystrokes and repeats actions"""
import argparse
import window_handler
import input_handler
import time

def main(args):
    # Wait for user acknowledgement.
    input('Press ENTER to start recording. Then x to stop recording once finished.')

    # Find window of interest.
    win = window_handler.find_window('RuneLite')
    
    # Bring it into focus.
    win.minimize()
    win.restore()

    # Record mouse inputs.
    raw_input = input_handler.record_mouse_input()

    # Filter mouse inputs.
    filt_inputs = input_handler.filter_clicks(raw_input)

    # Wait for user confirmation.
    print('Waiting for 5s delay before replaying input.')
    time.sleep(5)

    # Replay input.
    input_handler.replay_inputs(filt_inputs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required positional argument
    #parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    #parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    #parser.add_argument("-n", "--name", action="store", dest="name")

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