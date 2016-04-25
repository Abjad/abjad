# -*- coding: utf-8 -*-
import os
from abjad import abjad_configuration
from abjad.demos import desordre


def test_demos_desordre_01():

    lilypond_file = desordre.make_desordre_lilypond_file()
