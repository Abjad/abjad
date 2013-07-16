from abjad import *


def test_Selection_get_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        staff)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert staff[:].get(Measure, 0) is staff[0]
    assert staff[:].get(Measure, 1) is staff[1]
    assert staff[:].get(Measure, 2) is staff[2]


def test_Selection_get_02():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        staff)

    assert staff[:].get(Measure, -1) is staff[2]
    assert staff[:].get(Measure, -2) is staff[1]
    assert staff[:].get(Measure, -3) is staff[0]


def test_Selection_get_03():
    '''Read forwards for positive n.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
      {
            \time 2/8
            c'8
            d'8
      }
      {
            \time 2/8
            e'8
            f'8
      }
      {
            \time 2/8
            g'8
            a'8
      }
    }
    '''

    assert staff[:].get(leaftools.Leaf, 0) is staff[0][0]
    assert staff[:].get(leaftools.Leaf, 1) is staff[0][1]
    assert staff[:].get(leaftools.Leaf, 2) is staff[1][0]
    assert staff[:].get(leaftools.Leaf, 3) is staff[1][1]
    assert staff[:].get(leaftools.Leaf, 4) is staff[2][0]
    assert staff[:].get(leaftools.Leaf, 5) is staff[2][1]


def test_Selection_get_04():
    '''Read backwards for negative n.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
      {
            \time 2/8
            c'8
            d'8
      }
      {
            \time 2/8
            e'8
            f'8
      }
      {
            \time 2/8
            g'8
            a'8
      }
    }
    '''

    assert staff[:].get(leaftools.Leaf, -1) is staff[2][1]
    assert staff[:].get(leaftools.Leaf, -2) is staff[2][0]
    assert staff[:].get(leaftools.Leaf, -3) is staff[1][1]
    assert staff[:].get(leaftools.Leaf, -4) is staff[1][0]
    assert staff[:].get(leaftools.Leaf, -5) is staff[0][1]
    assert staff[:].get(leaftools.Leaf, -6) is staff[0][0]
