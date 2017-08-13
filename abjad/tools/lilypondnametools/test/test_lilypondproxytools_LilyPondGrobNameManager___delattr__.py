import abjad


def test_lilypondproxytools_LilyPondGrobNameManager___delattr___01():

    note = abjad.Note("c'4")
    abjad.override(note).accidental.color = 'red'
    abjad.override(note).beam.positions = (-6, -6)
    abjad.override(note).dots.thicknes = 2

    assert format(note) == abjad.String.normalize(
        r'''
        \once \override Accidental.color = #red
        \once \override Beam.positions = #'(-6 . -6)
        \once \override Dots.thicknes = #2
        c'4
        '''
        )

    del(abjad.override(note).accidental)
    del(abjad.override(note).beam)

    assert format(note) == abjad.String.normalize(
        r'''
        \once \override Dots.thicknes = #2
        c'4
        '''
        )


def test_lilypondproxytools_LilyPondGrobNameManager___delattr___02():
    r'''Delete LilyPond abjad.Rest grob abjad.override.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).rest.transparent = True
    del(abjad.override(staff).rest)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_lilypondproxytools_LilyPondGrobNameManager___delattr___03():
    r'''Delete LilyPond abjad.TimeSignature grob abjad.override.
    '''

    note = abjad.Note("c'4")
    abjad.override(note).time_signature.color = 'red'
    abjad.override(note).time_signature.transparent = True
    del(abjad.override(note).time_signature)

    assert format(note) == "c'4"
