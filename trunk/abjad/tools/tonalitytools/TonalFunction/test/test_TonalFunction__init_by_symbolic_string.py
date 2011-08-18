from abjad import *
from abjad.tools import tonalitytools


def test_TonalFunction__init_by_symbolic_string_01():

    tonal_function = tonalitytools.TonalFunction('bII')
    correct = tonalitytools.TonalFunction(('flat', 2), 'major', 5, 0)
    assert tonal_function == correct

    tonal_function = tonalitytools.TonalFunction('bII6')
    correct = tonalitytools.TonalFunction(('flat', 2), 'major', 5, 1)
    assert tonal_function == correct

    tonal_function = tonalitytools.TonalFunction('bII6/4')
    correct = tonalitytools.TonalFunction(('flat', 2), 'major', 5, 2)
    assert tonal_function == correct


def test_TonalFunction__init_by_symbolic_string_02():

    tonal_function = tonalitytools.TonalFunction('V7')
    correct = tonalitytools.TonalFunction(5, 'dominant', 7, 0)
    assert tonal_function == correct

    tonal_function = tonalitytools.TonalFunction('V6/5')
    correct = tonalitytools.TonalFunction(5, 'dominant', 7, 1)
    assert tonal_function == correct

    tonal_function = tonalitytools.TonalFunction('V4/3')
    correct = tonalitytools.TonalFunction(5, 'dominant', 7, 2)
    assert tonal_function == correct

    tonal_function = tonalitytools.TonalFunction('V4/2')
    correct = tonalitytools.TonalFunction(5, 'dominant', 7, 3)
    assert tonal_function == correct


def test_TonalFunction__init_by_symbolic_string_03():

    tonal_function = tonalitytools.TonalFunction('V7/4-3')
    correct = tonalitytools.TonalFunction(5, 'dominant', 7, 0, (4, 3))
    assert tonal_function == correct

    tonal_function = tonalitytools.TonalFunction('V6/5/4-3')
    correct = tonalitytools.TonalFunction(5, 'dominant', 7, 1, (4, 3))
    assert tonal_function == correct


def test_TonalFunction__init_by_symbolic_string_04():

    tonal_function = tonalitytools.TonalFunction('vi6/5')
    correct = tonalitytools.TonalFunction(6, 'minor', 7, 1)
    assert tonal_function == correct
