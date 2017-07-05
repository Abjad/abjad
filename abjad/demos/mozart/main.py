# -*- coding: utf-8 -*-
#! /usr/bin/env python


if __name__ == '__main__':
    import abjad
    from abjad.demos import mozart
    lilypond_file = mozart.make_mozart_lilypond_file()
    abjad.show(lilypond_file)
