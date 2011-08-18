from abjad import *
from abjad.tools import tonalitytools


def test_Scale___init___01():
    '''Init with tonic and mode strings.'''

    scale = tonalitytools.Scale('g', 'major')
    assert scale.key_signature == contexttools.KeySignatureMark('g', 'major')


def test_Scale___init___02():
    '''Init with key signature instance.'''

    key_signature = contexttools.KeySignatureMark('g', 'major')
    scale = tonalitytools.Scale(key_signature)
    assert scale.key_signature == contexttools.KeySignatureMark('g', 'major')


def test_Scale___init___03():
    '''Init with other scale instance.'''

    scale = tonalitytools.Scale('g', 'major')
    new = tonalitytools.Scale(scale)
    assert new.key_signature == contexttools.KeySignatureMark('g', 'major')
