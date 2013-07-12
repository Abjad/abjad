#! /usr/bin/env python

if __name__ == '__main__':
    from abjad.demos import desordre
    from abjad.tools import iotools
    lilypond_file = desordre.make_desordre_lilypond_file()
    iotools.show(lilypond_file)
