# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature___eq___01():

    key_signature1 = KeySignature('g', 'major')
    key_signature2 = KeySignature('g', 'major')
    key_signature3 = KeySignature('g', 'minor')

    assert key_signature1 == key_signature2
    assert not key_signature2 == key_signature3
    assert not key_signature3 == key_signature1
