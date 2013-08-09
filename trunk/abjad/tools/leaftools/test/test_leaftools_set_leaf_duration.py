# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_set_leaf_duration_01():
    r'''Change leaf to tied duration.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])

    r'''
    \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
    }
    '''

    leaftools.set_leaf_duration(voice[1], Duration(5, 32))

    r'''
    \new Voice {
      c'8 [
      d'8 ~
      d'32 ]
      e'8
      f'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ~
            d'32 ]
            e'8
            f'8
        }
        '''
        )


def test_leaftools_set_leaf_duration_02():
    r'''Change tied leaf to tied value.
    Duplicate ties are not created.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(voice[:2])
    spannertools.BeamSpanner(voice[:2])

    r'''
    \new Voice {
      c'8 [ ~
      c'8 ]
      c'8
      c'8
    }
    '''

    leaftools.set_leaf_duration(voice[1], Duration(5, 32))

    r'''
    \new Voice {
      c'8 [ ~
      c'8 ~
      c'32 ]
      c'8
      c'8
    }
    '''

    assert select(voice).is_well_formed()
    assert "\\new Voice {\n\tc'8 [ ~\n\tc'8 ~\n\tc'32 ]\n\tc'8\n\tc'8\n}"


def test_leaftools_set_leaf_duration_03():
    r'''Change leaf to nontied duration.
    Same as voice.written_duration = Duration(3, 16).
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])

    r'''
    \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
    }
    '''

    leaftools.set_leaf_duration(voice[1], Duration(3, 16))

    r'''
    \new Voice {
      c'8 [
      d'8. ]
      e'8
      f'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8. ]
            e'8
            f'8
        }
        '''
        )


def test_leaftools_set_leaf_duration_04():
    r'''Change leaf to tied duration without power-of-two denominator.
    Tuplet inserted over new tied notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])

    r'''
    \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
    }
    '''

    leaftools.set_leaf_duration(voice[1], Duration(5, 48))

    r'''
    \new Voice {
      c'8 [
      \times 2/3 {
            d'8 ~
            d'32 ]
      }
      e'8
      f'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \times 2/3 {
                d'8 ~
                d'32 ]
            }
            e'8
            f'8
        }
        '''
        )


def test_leaftools_set_leaf_duration_05():
    r'''Change leaf to untied duration without power-of-two denominator.
    Tuplet inserted over input leaf.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])

    r'''
    \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
    }
    '''

    leaftools.set_leaf_duration(voice[1], Duration(1, 12))

    r'''
    \new Voice {
      c'8 [
      \times 2/3 {
            d'8 ]
      }
      e'8
      f'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \times 2/3 {
                d'8 ]
            }
            e'8
            f'8
        }
        '''
        )


def test_leaftools_set_leaf_duration_06():
    r'''Change leaf with LilyPond multiplier to untied duration with power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    '''

    note = Note(0, (1, 8))
    note.lilypond_duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    leaftools.set_leaf_duration(note, Duration(1, 32))

    assert select(note).is_well_formed()
    assert note.lilypond_format == "c'8 * 1/4"


def test_leaftools_set_leaf_duration_07():
    r'''Change leaf with LilyPond multiplier to untied duration with power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    '''

    note = Note(0, (1, 8))
    note.lilypond_duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    leaftools.set_leaf_duration(note, Duration(3, 32))

    assert select(note).is_well_formed()
    assert note.lilypond_format == "c'8 * 3/4"


def test_leaftools_set_leaf_duration_08():
    r'''Change leaf with LilyPond multiplier to tied duration with power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    '''

    note = Note(0, (1, 8))
    note.lilypond_duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    leaftools.set_leaf_duration(note, Duration(5, 32))

    assert select(note).is_well_formed()
    assert note.lilypond_format == "c'8 * 5/4"


def test_leaftools_set_leaf_duration_09():
    r'''Change leaf with LilyPond multiplier to duration without power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    '''

    note = Note(0, (1, 8))
    note.lilypond_duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    leaftools.set_leaf_duration(note, Duration(1, 24))

    assert select(note).is_well_formed()
    assert note.lilypond_format == "c'8 * 1/3"


def test_leaftools_set_leaf_duration_10():
    r'''Change leaf with LilyPond multiplier.
    Change to tie-necessitating duration without power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    '''

    note = Note(0, (1, 8))
    note.lilypond_duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    leaftools.set_leaf_duration(note, Duration(5, 24))

    assert select(note).is_well_formed()
    assert note.lilypond_format == "c'8 * 5/3"
