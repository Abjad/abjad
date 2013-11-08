# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Scale___init___01():
    r'''Init with tonic and mode strings.
    '''

    scale = tonalanalysistools.Scale('g', 'major')
    assert scale.key_signature == marktools.KeySignature('g', 'major')


def test_tonalanalysistools_Scale___init___02():
    r'''Init with key signature instance.
    '''

    key_signature = marktools.KeySignature('g', 'major')
    scale = tonalanalysistools.Scale(key_signature)
    assert scale.key_signature == marktools.KeySignature('g', 'major')


def test_tonalanalysistools_Scale___init___03():
    r'''Init with other scale instance.
    '''

    scale = tonalanalysistools.Scale('g', 'major')
    new = tonalanalysistools.Scale(scale)
    assert new.key_signature == marktools.KeySignature('g', 'major')
