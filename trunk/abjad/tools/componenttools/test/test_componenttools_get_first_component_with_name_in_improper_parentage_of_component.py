from abjad import *


def test_componenttools_get_first_component_with_name_in_improper_parentage_of_component_01():
    '''Get first component with name in improper parentage of component.
    '''

    score = Score([Staff("c'4 d'4 e'4 f'4")])
    score.name = 'The Score'
    leaf = score.leaves[0]

    root = componenttools.get_first_component_with_name_in_improper_parentage_of_component(leaf, 'The Score')
    assert root is score


def test_componenttools_get_first_component_with_name_in_improper_parentage_of_component_02():
    '''Return none when no component with name is found in improper parentage of component.
    '''

    note = Note("c'4")
    score = componenttools.get_first_component_with_name_in_improper_parentage_of_component(note, 'The Score')

    assert score is None
