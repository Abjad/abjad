# -*- encoding: utf-8 -*-
from abjad import *


def test_stringtools_string_to_accent_free_snake_case_01():

    assert stringtools.string_to_accent_free_snake_case('Déja vu') == 'deja_vu'
