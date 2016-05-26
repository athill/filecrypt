import os, sys

from cli import Cli


if __name__ == "__main__":
    try:
        # cli = Cli()
        # cli.main()
        Cli.main()
    except KeyboardInterrupt:
        print('\nProcess interrupted by user')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) 