# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature___eq___01():

    ks1 = indicatortools.KeySignature('g', 'major')
    ks2 = indicatortools.KeySignature('g', 'major')
    ks3 = indicatortools.KeySignature('g', 'minor')

    assert ks1 == ks2
    assert not ks2 == ks3
    assert not ks3 == ks1
