# -*- encoding: utf-8 -*-
from abjad import *


def test_stringtools_string_to_strict_directory_name_01():

    assert stringtools.string_to_strict_directory_name('Déja vu') == 'deja_vu'
