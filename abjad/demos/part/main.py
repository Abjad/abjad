# -*- coding: utf-8 -*-
#! /usr/bin/env python

if __name__ == '__main__':
    from abjad import show
    from abjad.demos import part
    lilypond_file = part.make_part_lilypond_file()
    show(lilypond_file)
