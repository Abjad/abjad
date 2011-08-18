from abjad import *


def test_componenttools_get_likely_multiplier_of_components_01():
    '''Components were likely multiplied by 5/4.'''

    t = Staff("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(5, 4))
    assert componenttools.get_likely_multiplier_of_components(t[:]) == Duration(5, 4)


def test_componenttools_get_likely_multiplier_of_components_02():
    '''Components were likely multiplied by 3/2.'''

    t = Staff("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(3, 2))
    assert componenttools.get_likely_multiplier_of_components(t[:]) == Duration(3, 2)


def test_componenttools_get_likely_multiplier_of_components_03():
    '''Components were likely multiplied by 7/4.'''

    t = Staff("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(7, 4))
    assert componenttools.get_likely_multiplier_of_components(t[:]) == Duration(7, 4)


def test_componenttools_get_likely_multiplier_of_components_04():
    '''Components likely multiplier not recoverable.'''

    t = Staff("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(2))
    assert componenttools.get_likely_multiplier_of_components(t[:]) == Duration(1)


def test_componenttools_get_likely_multiplier_of_components_05():
    '''Components likely multiplier not recoverable.'''

    t = Staff("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(1, 2))
    assert componenttools.get_likely_multiplier_of_components(t[:]) == Duration(1)


def test_componenttools_get_likely_multiplier_of_components_06():
    '''Components multiplier recoverable only to within one power of two.'''

    t = Staff("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(10, 4))
    assert not componenttools.get_likely_multiplier_of_components(t[:]) == Duration(10, 4)
    assert componenttools.get_likely_multiplier_of_components(t[:]) == Duration(5, 4)


def test_componenttools_get_likely_multiplier_of_components_07():
    '''Return none when more than one likely multiplier.'''

    t = Staff(notetools.make_notes([0], [(1, 8), (7, 32)]))
    assert componenttools.get_likely_multiplier_of_components(t[:]) is None
