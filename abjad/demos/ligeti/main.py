# -*- coding: utf-8 -*-
#! /usr/bin/env python
import abjad


if __name__ == '__main__':
    lilypond_file = abjad.demos.ligeti.make_desordre_lilypond_file()
    abjad.show(lilypond_file)
