# -*- encoding: utf-8 -*-
from abjad import *


def test_stringtools_string_to_accent_free_underscored_delimited_lowercase_01():

    assert stringtools.string_to_accent_free_underscored_delimited_lowercase('Déja vu') == 'deja_vu'
