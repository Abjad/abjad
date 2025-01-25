#! /usr/bin/env python
import sys

import abjad


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = ""
    startup_string = f"Abjad {abjad.__version__}"
    commands = f"import abjad; print({startup_string!r});"
    string = rf'''python -i {file_name} -c "{commands}"'''
    abjad.io.spawn_subprocess(string)


if __name__ == "__main__":
    main()
