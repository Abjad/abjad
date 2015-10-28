# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_interlace_sequences_01():

    k = range(100, 103)
    l = range(200, 201)
    m = range(300, 303)
    n = range(400, 408)
    result = sequencetools.interlace_sequences([k, l, m, n])

    assert result == [
        100, 200, 300, 400, 101, 301, 401, 102, 302, 
        402, 403, 404, 405, 406, 407]


def test_sequencetools_interlace_sequences_02():

    string_1 = 'introductory'
    string_2 = 'text'

    result = sequencetools.interlace_sequences([string_1, string_2])
    result = ''.join(result)

    assert result == 'itnetxrtoductory'