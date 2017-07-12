# -*- coding: utf-8 -*-
#! /usr/bin/env python
import abjad


if __name__ == '__main__':
    lilypond_file = abjad.demos.part.make_part_lilypond_file()
    abjad.show(lilypond_file)
