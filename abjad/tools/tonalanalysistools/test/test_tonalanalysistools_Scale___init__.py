# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_Scale___init___01():
    r'''Initialize with tonic and mode strings.
    '''

    scale = tonalanalysistools.Scale('g', 'major')
    assert scale.key_signature == KeySignature('g', 'major')


def test_tonalanalysistools_Scale___init___02():
    r'''Initialize with key signature instance.
    '''

    key_signature = KeySignature('g', 'major')
    scale = tonalanalysistools.Scale(key_signature)
    assert scale.key_signature == KeySignature('g', 'major')


def test_tonalanalysistools_Scale___init___03():
    r'''Initialize with other scale instance.
    '''

    scale = tonalanalysistools.Scale('g', 'major')
    new = tonalanalysistools.Scale(scale)
    assert new.key_signature == KeySignature('g', 'major')
