# -*- encoding: utf-8 -*-
from abjad import *


def test_iotools_string_to_strict_directory_name_01():

    assert iotools.string_to_strict_directory_name('Déja vu') == 'deja_vu'
