# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_to_accent_free_snake_case_01():

    assert stringtools.to_accent_free_snake_case('Déja vu') == 'deja_vu'
