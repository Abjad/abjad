# -*- encoding: utf-8 -*-
from abjad import *


def test_foo_01():

    assert iotools.string_to_strict_directory_name('Déja vu') == 'deja_vu'
