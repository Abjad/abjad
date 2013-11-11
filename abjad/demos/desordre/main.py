# -*- encoding: utf-8 -*-
#! /usr/bin/env python

if __name__ == '__main__':
    from abjad.demos import desordre
    from abjad.tools import systemtools
    lilypond_file = desordre.make_desordre_lilypond_file()
    topleveltools.show(lilypond_file)
