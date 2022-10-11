"""Autoclicker which records keystrokes and repeats actions"""
import window_util


def main(args):
    # 1. Find window of interest.
    win = window_util.find_window('RuneLite')
    
    # 2. Bring it into focus.
    win.restore()

    # 3. Record mouse inputs.
    window_util.record_mouse_inputs()
    


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