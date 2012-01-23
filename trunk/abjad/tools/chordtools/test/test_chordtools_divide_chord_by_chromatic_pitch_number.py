from abjad import *


def test_chordtools_divide_chord_by_chromatic_pitch_number_01():
    '''Chord split by number only; empty bass.
    '''

    chord = Chord("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('d', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(chord, pitch)
    assert isinstance(treble, Chord)
    assert treble.format == "<d' ef' e'>4"
    assert isinstance(bass, Rest)
    assert bass.format == 'r4'
    assert chord is not treble
    assert chord is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_02():
    '''Chord split by number only; one-note bass.
    '''

    t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
    pitch = pitchtools.NamedChromaticPitch('ef', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, pitch)
    assert isinstance(treble, Chord)
    assert treble.format == Chord([3, 4], (1, 4)).format
    assert isinstance(bass, Note)
    assert bass.format == Note(2, (1, 4)).format
    assert t is not treble
    assert t is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_03():
    '''Chord split by number only; one-note treble.
    '''

    t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
    pitch = pitchtools.NamedChromaticPitch('e', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, pitch)
    assert isinstance(treble, Note)
    assert treble.format == Note(4, (1, 4)).format
    assert isinstance(bass, Chord)
    assert bass.format == Chord([2, 3], (1, 4)).format
    assert t is not treble
    assert t is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_04():
    '''Chord split by number only; empty treble.
    '''

    t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
    pitch = pitchtools.NamedChromaticPitch('f', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, pitch)
    assert isinstance(treble, Rest)
    assert treble.format == Rest((1, 4)).format
    assert isinstance(bass, Chord)
    assert bass.format == Chord([2, 3, 4], (1, 4)).format
    assert t is not treble
    assert t is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_05():
    '''Typographically crossed split by number only.
    '''

    t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
    pitch = pitchtools.NamedChromaticPitch('f', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, pitch)
    assert isinstance(treble, Chord)
    assert treble.format == Chord([('es', 4), 7], (1, 4)).format
    assert treble.format == Chord([('es', 4), ('g', 4)], (1, 4)).format
    assert isinstance(bass, Chord)
    assert bass.format == Chord([('d', 4), ('ff', 4)], (1, 4)).format
    assert t is not treble
    assert t is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_06():
    '''Single note below pitch number split point.
    '''

    note = Note("c'4")
    pitch = pitchtools.NamedChromaticPitch('f', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(note, pitch)
    assert isinstance(treble, Rest)
    assert treble.format == Rest((1, 4)).format
    assert isinstance(bass, Note)
    assert bass.format == Note("c'4").format
    assert note is not treble
    assert note is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_07():
    '''Single note at pitch number split point.
    '''

    note = Note("c'4")
    pitch = pitchtools.NamedChromaticPitch('c', 4)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(note, pitch)
    assert isinstance(treble, Note)
    assert treble.format == Note("c'4").format
    assert isinstance(bass, Rest)
    assert bass.format == Rest((1, 4)).format
    assert note is not treble
    assert note is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_08():
    '''Single note above pitch number split point.
    '''

    note = Note("c'4")
    pitch = pitchtools.NamedChromaticPitch('f', 3)
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(note, pitch)
    assert isinstance(treble, Note)
    assert treble.format == Note("c'4").format
    assert isinstance(bass, Rest)
    assert bass.format == Rest((1, 4)).format
    assert note is not treble
    assert note is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_09():
    '''Rest splits into two new rests.
    '''

    t = Rest((1, 4))
    pitch = pitchtools.NamedChromaticPitch(('b', 3))
    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, pitch)
    assert isinstance(treble, Rest)
    assert treble.format == Rest((1, 4)).format
    assert isinstance(bass, Rest)
    assert bass.format == Rest((1, 4)).format
    assert t is not treble
    assert t is not bass
    assert treble is not bass


def test_chordtools_divide_chord_by_chromatic_pitch_number_10():
    '''Split copies over note head coloring.
    '''

    t = Chord([0, 1, 2, 3], (1, 4))
    t[0].tweak.color = 'red'
    t[1].tweak.color = 'red'
    t[2].tweak.color = 'blue'
    t[3].tweak.color = 'blue'

    r'''
    <
        \tweak #'color #red
        c'
        \tweak #'color #red
        cs'
        \tweak #'color #blue
        d'
        \tweak #'color #blue
        ef'
    >4
    '''

    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, 2)

    r'''
    <
        \tweak #'color #blue
        d'
        \tweak #'color #blue
        ef'
    >4
    '''

    assert componenttools.is_well_formed_component(treble)
    assert treble.format == "<\n\t\\tweak #'color #blue\n\td'\n\t\\tweak #'color #blue\n\tef'\n>4"

    r'''
    <
        \tweak #'color #red
        c'
        \tweak #'color #red
        cs'
    >4    
    '''

    assert componenttools.is_well_formed_component(bass)
    assert bass.format == "<\n\t\\tweak #'color #red\n\tc'\n\t\\tweak #'color #red\n\tcs'\n>4"


def test_chordtools_divide_chord_by_chromatic_pitch_number_11():
    '''Copy up-markup to treble and down-markup to bass.
    '''

    t = Chord([-11, 2, 5], (1, 4))
    markuptools.Markup('UP', 'up')(t)
    markuptools.Markup('DOWN', 'down')(t)

    "<cs d' f'>4 ^ \markup { UP } _ \markup { DOWN }"

    treble, bass = chordtools.divide_chord_by_chromatic_pitch_number(t, 0)

    "<d' f'>4 ^ \markup { UP }"

    assert componenttools.is_well_formed_component(treble)
    assert treble.format == "<d' f'>4 ^ \\markup { UP }"

    "cs4 _ \markup { DOWN }"

    assert componenttools.is_well_formed_component(bass)
    assert bass.format == 'cs4 _ \\markup { DOWN }'
