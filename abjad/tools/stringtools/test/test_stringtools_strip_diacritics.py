# -*- coding: utf-8 -*-
import sys
from abjad import *


def test_stringtools_strip_diacritics_01():

    if sys.version_info[0] == 2:
        binary_string = 'Dvo\xc5\x99\xc3\xa1k'
    else:
        binary_string = 'Dvořák'
    ascii_string = stringtools.strip_diacritics(binary_string)

    assert ascii_string == 'Dvorak'
