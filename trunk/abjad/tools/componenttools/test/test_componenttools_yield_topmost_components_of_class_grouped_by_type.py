from abjad import *


def test_componenttools_yield_topmost_components_of_class_grouped_by_type_01():
    '''Group notes.
    '''

    staff = Staff(leaftools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
    t = list(componenttools.yield_topmost_components_of_class_grouped_by_type(
        staff, Note))

    assert t == [(staff[0], staff[1], staff[2]), (staff[5], staff[6])]


def test_componenttools_yield_topmost_components_of_class_grouped_by_type_02():
    '''Group chords.
    '''

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8")
    staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    chord_groups = \
        componenttools.yield_topmost_components_of_class_grouped_by_type(
        staff, Chord)
    chord_groups = list(chord_groups)

    assert chord_groups[0] == (staff[4], staff[5])
    assert chord_groups[1] == (staff[10], staff[11])


def test_componenttools_yield_topmost_components_of_class_grouped_by_type_03():
    '''Group rests.
    '''

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8")
    staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    rest_groups = \
        componenttools.yield_topmost_components_of_class_grouped_by_type(
        staff, Rest)
    rest_groups = list(rest_groups)

    assert rest_groups[0] == (staff[2], staff[3])
    assert rest_groups[1] == (staff[8], staff[9])


def test_componenttools_yield_topmost_components_of_class_grouped_by_type_04():
    '''Group skips.
    '''

    staff = Staff("c'8 d'8 s8 s8 <e' g'>8 <f' a'>8")
    staff.extend("g'8 a'8 s8 s8 <b' d''>8 <c'' e''>8")

    skip_groups = \
        componenttools.yield_topmost_components_of_class_grouped_by_type(
        staff, skiptools.Skip)
    skip_groups = list(skip_groups)

    assert skip_groups[0] == (staff[2], staff[3])
    assert skip_groups[1] == (staff[8], staff[9])


def test_componenttools_yield_topmost_components_of_class_grouped_by_type_05():
    '''Group notes.
    '''

    staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8")
    staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    note_groups = \
        componenttools.yield_topmost_components_of_class_grouped_by_type(
        staff, Note)
    note_groups = list(note_groups)

    assert note_groups[0] == (staff[0], staff[1])
    assert note_groups[1] == (staff[6], staff[7])
