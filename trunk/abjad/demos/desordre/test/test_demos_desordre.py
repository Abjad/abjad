# -*- encoding: utf-8 -*-
from abjad import abjad_configuration
from abjad.demos import desordre
import os


def test_demos_desordre_01():

    lilypond_file = desordre.make_desordre_lilypond_file()
