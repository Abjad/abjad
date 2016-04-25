# -*- coding: utf-8 -*-
from abjad import *
from abjad.demos.ferneyhough.make_lilypond_file import make_lilypond_file


def test_demos_ferneyhough_01():

    lilypond_file = make_lilypond_file(Duration(1, 4), 10, 6)
