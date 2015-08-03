# -*- encoding: utf-8 -*-
#! /usr/bin/env python

if __name__ == '__main__':
    from abjad import show
    from abjad.demos import bartok
    lilypond_file = bartok.make_bartok_score()
    show(lilypond_file)