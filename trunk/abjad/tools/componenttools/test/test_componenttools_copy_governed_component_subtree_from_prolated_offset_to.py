from abjad import *


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_01():
    '''Container.'''

    t = Container("c'8 d'8 e'8")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (3, 16))

    r'''
    {
    c'8
    d'16
    }
    '''

    assert new.format == "{\n\tc'8\n\td'16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to002():
    '''Container with rest.'''

    t = Container("c'8 d'8 e'8")
    rest = Rest(t[1])
    componenttools.move_parentage_and_spanners_from_components_to_components(t[1:2], [rest])
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (3, 16))

    r'''
    {
    c'8
    r16
    }
    '''

    assert new.format == "{\n\tc'8\n\tr16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_03():
    '''Clone measure.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (3, 16))

    r'''
    {
    \time 3/16
    c'8
    d'16
    }
    '''

    assert new.format == "{\n\t\\time 3/16\n\tc'8\n\td'16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_04():
    '''Fixed duration tuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (1, 8))

    r'''
    \times 2/3 {
    c'8
    d'16
    }
    '''

    assert new.format == "\\times 2/3 {\n\tc'8\n\td'16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_05():
    '''Fixed multiplier tuplet.'''

    t = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (1, 8))

    r'''
    \times 2/3 {
    c'8
    d'16
    }
    '''

    assert new.format == "\\times 2/3 {\n\tc'8\n\td'16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_06():
    '''Voice.'''

    t = Voice("c'8 d'8 e'8")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (3, 16))

    r'''
    \new Voice {
    c'8
    d'16
    }
    '''

    assert new.format == "\\new Voice {\n\tc'8\n\td'16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_07():
    '''Staff.'''

    t = Staff("c'8 d'8 e'8")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (3, 16))

    r'''
    \new Staff {
    c'8
    d'16
    }
    '''

    assert new.format == "\\new Staff {\n\tc'8\n\td'16\n}"


# Anatomy of the tests:
#   there are five different timepoints relative to the timespan of a note:
#     1. 'before', ie a negative number
#     2. 'start', ie 0 which is the startpoint of the timespan
#     3. 'mid', ie some value y such that 0 < y < t.prolated_duration
#     4. 'stop', ie t.prolated_duration
#     5. 'after', ie some value z such that t.prolated_duration < z


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_08():
    '''Start-to-mid clean cut.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (1, 8))
    assert new.format == "c'8"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_09():
    '''Start-to-mid jagged cut.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (1, 12))
    parent = new._parentage.parent

    r'''
    \times 2/3 {
        c'8
    }
    '''

    assert parent.format == "\\times 2/3 {\n\tc'8\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_10():
    '''Mid-mid jagged cut.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, (1, 12), (2, 12))
    parent = new._parentage.parent

    r'''
    \times 2/3 {
        c'8
    }
    '''

    assert parent.format == "\\times 2/3 {\n\tc'8\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_11():
    '''Mid-to-stop jagged cut.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, (1, 6), (1, 4))
    parent = new._parentage.parent

    r'''
    \times 2/3 {
        c'8
    }
    '''

    assert parent.format == "\\times 2/3 {\n\tc'8\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_12():
    '''Start-to-after clean cut.'''
    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (1, 2))
    assert new.format == "c'4"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_13():
    '''Mid-to-after clean cut.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, (1, 8), (1, 2))
    assert new.format == "c'8"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_14():
    '''Mid-to-after jagged cut.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, (2, 12), (1, 2))
    parent = new._parentage.parent

    r'''
    \times 2/3 {
        c'8
    }
    '''

    assert parent.format == "\\times 2/3 {\n\tc'8\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_15():
    '''Before-to-after.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, (-1, 4), (1, 2))
    assert new.format == "c'4"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_16():
    '''Start-to-mid jagged.'''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (5, 24))
    parent = new._parentage.parent

    r'''
    \times 2/3 {
        c'4 ~
        c'16
    }
    '''

    assert parent.format == "\\times 2/3 {\n\tc'4 ~\n\tc'16\n}"


def test_componenttools_copy_governed_component_subtree_from_prolated_offset_to_17():
    '''Start-to-mid jagged. '''

    t = Note("c'4")
    new = componenttools.copy_governed_component_subtree_from_prolated_offset_to(t, 0, (1, 5))
    parent = new._parentage.parent

    r'''
    \times 4/5 {
        c'4
    }
    '''
